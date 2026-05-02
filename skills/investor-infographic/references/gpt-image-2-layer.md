# GPT Image 2 Layer

Use this only when the user wants richer AI-generated visual assets or when the current HTML/SVG sketch references need a more polished illustration layer.

## Official Model Notes

- OpenAI's image generation docs describe `gpt-image-2` as the latest GPT Image model for generating and editing images.
- Use the Image API for one-shot asset generation or edits.
- Use the Responses API image generation tool for multi-turn or conversational image workflows; in that API, use a mainline model such as `gpt-5.4` as the `model` value and the hosted `image_generation` tool. Do not put `gpt-image-2` directly in the Responses API `model` field.
- `gpt-image-2` supports flexible image sizes up to a 3840px maximum edge, with both edges multiples of 16, ratio no more than 3:1, and total pixels no more than 8,294,400.
- `gpt-image-2` does not currently support transparent backgrounds.
- GPT Image models can still struggle with precise text, exact layout, recurring consistency, and structured composition. Keep final financial text and charts in deterministic renderers.
- Using GPT Image models may require OpenAI API organization verification.

Reference docs:

- `https://developers.openai.com/api/docs/guides/image-generation`
- `https://developers.openai.com/api/docs/guides/tools-image-generation`

## Where It Fits In This Skill

Use GPT Image 2 before the final HTML/SVG screenshot step:

1. Research and write the data module as usual.
2. Decide the deterministic final layout in HTML/SVG.
3. Generate any visual asset needed for the layout: portrait, background, symbolic object, scene, paper texture, or mood illustration.
4. Place the generated asset into the HTML as an `<img>` or background layer.
5. Keep numbers, Chinese labels, legends, bars, pies, and captions in SVG/HTML text.
6. Screenshot with Chrome at 4x.

## Prompt Pattern

For an investor portrait or scene:

```text
Draw a refined hand-drawn editorial illustration for a Chinese investment infographic.
Subject: <investor or company>.
Visual metaphor: <moat / compounding snowball / AI factory / global payments network>.
Style: warm paper background, ink-and-watercolor linework, clean finance editorial style, no readable text, no logos unless explicitly provided.
Composition: leave empty space on the right for charts and Chinese annotations.
Palette: <2-3 colors that match the target sketch>.
Output: landscape, high detail.
```

For editing an existing sketch asset:

```text
Edit this image to make it feel like a polished hand-drawn Chinese finance infographic background.
Preserve the overall composition and empty areas for charts.
Remove or avoid readable text.
Use <palette>.
```

## Helper Script

Script path: `/Users/jiangming/.codex/skills/investor-infographic/scripts/generate_gpt_image.py`

Prerequisites:

- `OPENAI_API_KEY` set in the shell environment.
- Python `openai` package installed in the active environment.

Example:

```bash
python3 /Users/jiangming/.codex/skills/investor-infographic/scripts/generate_gpt_image.py \
  --prompt-file /tmp/prompt.txt \
  --output "/Users/jiangming/持仓分析/<folder>/<slug>_gpt_image_asset.png" \
  --size 1536x1024 \
  --quality high
```

Use `--size 3840x2160` only for final high-resolution assets and expect higher cost/latency.
