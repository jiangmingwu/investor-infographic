#!/usr/bin/env python3
"""Fetch reviewed long-term stock-price snapshots for post-Chevron profiles."""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


OUTPUT = Path("/Users/jiangming/templates/data/market_history/post_chevron_stock_history_20260715.json")
PERIOD1 = -252322200
PERIOD2 = 1784160000
USER_AGENT = "Mozilla/5.0"

CONFIG = {
    "pg": {"symbol": "PG", "listing_note": "1890年股份化 · NYSE: PG", "listing_source": "https://us.pg.com/pg-history/"},
    "roche": {"symbol": "RO.SW", "listing_note": "SIX: RO普通股 · 公开序列自1995年", "listing_source": "https://www.roche.com/investors/faq_investors"},
    "homedepot": {"symbol": "HD", "listing_note": "1981年NASDAQ首次上市 · 后转NYSE", "listing_source": "https://corporate.homedepot.com/page/history"},
    "hsbc": {"symbol": "HSBC", "listing_note": "NYSE ADR 1999年上市", "listing_source": "https://www.hsbc.com/investors/shareholder-and-dividend-information/share-information/"},
    "arm": {"symbol": "ARM", "listing_note": "NASDAQ 2023年重新上市", "listing_source": "https://newsroom.arm.com/news/arm-ipo"},
    "palantir": {"symbol": "PLTR", "listing_note": "2020年直接上市 · 2024年转NASDAQ", "listing_source": "https://investors.palantir.com/"},
    "agriculturalbank": {"symbol": "1288.HK", "listing_note": "2010年沪港同步上市 · HKEX: 1288", "listing_source": "https://www.abchina.com/en/AboutUs/"},
    "merck": {"symbol": "MRK", "listing_note": "NYSE: MRK · 公开序列自1962年", "listing_source": "https://www.merck.com/investor-relations/investor-resources/"},
    "icbc": {"symbol": "1398.HK", "listing_note": "2006年沪港同步上市 · HKEX: 1398", "listing_source": "https://www.icbc-ltd.com/"},
    "goldmansachs": {"symbol": "GS", "listing_note": "NYSE 1999年首次公开上市", "listing_source": "https://www.goldmansachs.com/our-firm/history"},
    "novartis": {"symbol": "NVS", "listing_note": "1996年合并成立 · NYSE ADR", "listing_source": "https://www.novartis.com/about/history"},
    "astrazeneca": {"symbol": "AZN", "listing_note": "1999年合并成立 · 当前NASDAQ: AZN", "listing_source": "https://www.astrazeneca.com/our-company/history.html", "floor": "1999-04-06"},
    "philipmorris": {"symbol": "PM", "listing_note": "NYSE 2008年分拆独立上市", "listing_source": "https://www.pmi.com/investor-relations/overview"},
    "kla": {"symbol": "KLAC", "listing_note": "NASDAQ公开价格序列自1980年", "listing_source": "https://ir.kla.com/"},
    "gevernova": {"symbol": "GEV", "listing_note": "NYSE 2024年分拆独立上市", "listing_source": "https://www.gevernova.com/investors"},
    "rbc": {"symbol": "RY", "listing_note": "NYSE美元价格序列自1995年", "listing_source": "https://www.rbc.com/investor-relations/share-information.html"},
    "ibm": {"symbol": "IBM", "listing_note": "NYSE 1916年上市", "listing_source": "https://www.ibm.com/history/nyse"},
    "dell": {"symbol": "DELL", "listing_note": "NYSE 2018年重返公开市场", "listing_source": "https://investors.delltechnologies.com/", "floor": "2018-12-28"},
}


def chart_url(symbol: str) -> str:
    encoded = urllib.parse.quote(symbol, safe="")
    return (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}"
        f"?period1={PERIOD1}&period2={PERIOD2}&interval=1wk"
        "&events=div%2Csplits&includeAdjustedClose=true"
    )


def fetch_chart(symbol: str) -> tuple[dict, str]:
    url = chart_url(symbol)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
            return payload["chart"]["result"][0], url
        except Exception as exc:  # network retry is intentionally narrow
            error = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Yahoo Finance fetch failed for {symbol}: {error}")


def valid_prices(result: dict, floor: str | None = None) -> list[tuple[dt.date, float]]:
    values = []
    closes = result["indicators"]["quote"][0]["close"]
    floor_date = dt.date.fromisoformat(floor) if floor else None
    for timestamp, close in zip(result["timestamp"], closes):
        if close is None:
            continue
        date = dt.datetime.fromtimestamp(timestamp, dt.timezone.utc).date()
        if floor_date and date < floor_date:
            continue
        values.append((date, float(close)))
    if len(values) < 3:
        raise ValueError("stock-price history has fewer than three observations")
    return values


def display_series(values: list[tuple[dt.date, float]], fx_to_usd: float) -> list[list[object]]:
    duration = (values[-1][0] - values[0][0]).days / 365.25
    if duration <= 8:
        key = lambda item: (item[0].year, item[0].month)
    elif duration <= 20:
        key = lambda item: (item[0].year, (item[0].month - 1) // 3)
    else:
        key = lambda item: item[0].year
    buckets: dict[object, tuple[dt.date, float]] = {}
    for item in values:
        buckets[key(item)] = item
    chosen = [values[0], *buckets.values(), values[-1]]
    unique = []
    seen = set()
    for date, close in chosen:
        if date in seen:
            continue
        seen.add(date)
        unique.append([date.isoformat(), round(close * fx_to_usd, 4)])
    return sorted(unique)


def fx_snapshot() -> dict[str, dict[str, object]]:
    snapshot = {"USD": {"rate": 1.0, "date": "2026-07-15", "symbol": "USD"}}
    for currency, symbol in (("CHF", "CHFUSD=X"), ("HKD", "HKDUSD=X")):
        result, _ = fetch_chart(symbol)
        values = valid_prices(result)
        date, close = values[-1]
        snapshot[currency] = {"rate": close, "date": date.isoformat(), "symbol": symbol}
    return snapshot


def main() -> int:
    fx = fx_snapshot()
    histories = {}
    for slug, config in CONFIG.items():
        result, url = fetch_chart(config["symbol"])
        source_currency = result["meta"]["currency"]
        if source_currency not in fx:
            raise ValueError(f"unsupported source currency for {slug}: {source_currency}")
        rate = float(fx[source_currency]["rate"])
        values = valid_prices(result, config.get("floor"))
        series = display_series(values, rate)
        fx_date = str(fx[source_currency]["date"])
        if source_currency == "USD":
            currency_note = "原始行情为美元，无需换汇。"
        else:
            currency_note = (
                f"原始行情为{source_currency}；整段历史按2026年7月15日"
                f"{source_currency}/USD {rate:.4f}固定汇率换算，仅用于统一美元量纲。"
            )
        histories[slug] = {
            "symbol": config["symbol"],
            "listing_note": config["listing_note"],
            "listing_source": config["listing_source"],
            "source_name": "Yahoo Finance",
            "source_url": url,
            "source_currency": source_currency,
            "display_currency": "USD",
            "fx_to_usd": round(rate, 6),
            "fx_date": fx_date,
            "currency_note": currency_note,
            "price_basis": "拆股调整收盘价，不含股息再投资",
            "as_of": values[-1][0].isoformat(),
            "series_start": values[0][0].isoformat(),
            "series_end": values[-1][0].isoformat(),
            "series": series,
        }
        print(f"{slug}: {config['symbol']} {series[0][0]} -> {series[-1][0]} ({len(series)} points)")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(histories, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
