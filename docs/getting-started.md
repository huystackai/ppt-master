# Getting Started

The short path to your first deck, how to use everything around it — templates, live preview, animations, narration, voice cloning — and where to look when something goes wrong. Sections follow roughly the order you meet them in a real run. Each is the quick version; follow the **Full guide →** link for depth.

- [Start from a template](#start-from-a-template)
- [Generate your first deck](#generate-your-first-deck)
- [Live preview & visual edits](#live-preview--visual-edits)
- [Animations & transitions](#animations--transitions)
- [Narration & video](#narration--video)
- [Use a cloned voice](#use-a-cloned-voice)
- [When something goes wrong](#when-something-goes-wrong)

---

## Start from a template

**Optional.** By default PPT Master uses **free design** — you don't need a template, and you can skip to the next section. Reach for one only when a deck must reuse a fixed layout set or brand identity.

**To follow a sample, drag a PPTX, PDF, SVG, or slide screenshot into your agent's chat and say “use this as the design reference.”** Attach your content separately or explain which attachment supplies the content. The agent prepares the reference, extracts its visual rules, and follows them in the new editable deck. Times New Roman remains the default unless you ask to preserve the sample's font or choose another font.

For a **reusable template library**, explicitly request template creation:

```
You: Replicate this as a reusable template via /create-template: projects/brand/our_deck.pptx
```

That runs `pptx_template_import.py` and rebuilds the file into a reusable bundle — layout SVGs + `design_spec.md` + extracted theme colors, fonts, and images. See [Uploaded Slide References](../workflows/use-slide-reference.md) for one-off samples.

A created template lives in one of two places:

| Location | Path | Notes |
|---|---|---|
| **Registered in the skill library** | `templates/layouts/<id>/` | Global, reusable across every project; run `register_template.py` so it shows up when you ask "what templates are available?" |
| **Inside a project** | `projects/<project>/templates/` | Project-local; works by path, no registration needed |

Either way, you invoke it during generation by giving its **directory path** in chat — the workflow triggers on an explicit path only, never on a bare template name:

```
You: Make a deck from sources/report.pdf with template templates/layouts/academic_defense/
```

Full guide → [Templates Guide](./templates-guide.md)

---

## Generate your first deck

Copy the complete `ppt-master` folder into your agent's skills directory with Python 3.10+ available; see [Install](../README.md#install). On first use, the agent prepares the Python runtime automatically. The whole loop is three steps.

1. **Attach your source material** in chat or place it in your workspace — a PDF, DOCX, Markdown file, a URL, or just text you'll paste.
2. **Tell the AI in chat** what to turn into a deck (add a template path if you set one up above; otherwise it's free design):
   ```
   You: Make a deck from projects/q3-report/sources/report.pdf
   You: 把这份内容做成 PPT：<paste your text>
   ```
3. **Get an editable `.pptx`** at `exports/<name>_<timestamp>.pptx` — real DrawingML shapes, text boxes, and charts you can click and edit in PowerPoint, Keynote, WPS, or LibreOffice.

Before it starts, the AI confirms a short design spec (template, format, page count, …); from there it handles content analysis, layout, image acquisition, SVG generation, and export — the core loop everything else builds on.

---

## Live preview & visual edits

A browser preview opens at `http://localhost:5050` while the deck is being generated.

- **Watch pages render live** as the AI produces them.
- **Edit directly, no AI** — select an element to change its text, color, font, or size in the side panel; drag it to reposition, or nudge with the arrow keys (`Shift` = 10px). `Ctrl+Z` undoes. Edits preview instantly and write to `svg_output/` when you click **Apply changes**.
- **Or annotate for the AI** — click an element, type what you want changed, hit **Submit annotations**, then say "apply my annotations" in chat and the AI rewrites that region and re-exports the PPTX.

PPT Master was chat-only by design; visual editing was folded in after enough users asked for it (built on [@WodenJay](https://github.com/WodenJay)'s [PR #85](https://github.com/hugohe3/ppt-master/pull/85)).

Full guide → [Live Preview Workflow](../workflows/live-preview.md)

---

## Animations & transitions

Exported decks ship **page transitions** and **per-element entrance animations** as real OOXML — not embedded video. By default, elements cascade in on slide entry with no setup, and the deck plays natively in PowerPoint and Keynote with no extra tooling. Reach for customization only when you want a specific order, effect, or timing.

Full guide → [Animations & Transitions](../references/animations.md)

---

## Narration & video

Turn the speaker notes into per-slide voice narration, embed the audio back into the PPTX, and let PowerPoint export the deck as a synced-narration MP4 — no third-party tools.

```
You: Generate narration for this deck and re-export with audio embedded.
You: 给这个 PPT 生成音频
```

Narration defaults to `edge-tts` (about 90 locales); optional cloud providers cover higher-quality voices. The AI recommends a voice for the deck's language and asks once before generating.

Full guide → [Audio Narration & Video Export](./audio-narration.md)

---

## Use a cloned voice

Bring your own cloned voice from ElevenLabs / MiniMax / Qwen / CosyVoice and have the whole deck narrated in *your* voice (or a presenter's, with permission). Clone once in the provider's console, then pass the `voice_id` — PPT Master reads every slide's notes in that voice and embeds the result back into the PPTX.

Full guide → [Use a cloned voice](./audio-narration.md#use-a-cloned-voice)

---

## When something goes wrong

The [FAQ](./faq.md) is the living troubleshooting reference — continuously updated from real user reports. Quick pointers for the most common situations:

| Situation | First thing to try |
|---|---|
| The AI drifts or forgets a step | Ask it to re-read `SKILL.md`. |
| Visual quality disappoints | Switch to a large-context Claude model + `gpt-image-2` — the harness sets the floor, the model sets the ceiling. |
| Text overflows or elements overlap | Re-run that page, or fix it in live preview; see the [FAQ](./faq.md). |
| No image-generation API key | Zero-config web search still works as a fallback; see the [FAQ](./faq.md). |
| Animations or some effects look off in another app | The file is standard `.pptx` and opens in PowerPoint / Keynote / WPS / LibreOffice; element animations render most completely in PowerPoint 2016+ and Keynote, while older Office may downgrade some to plain Appear. |
| A long deck might blow the context window | Generation can run in split mode; details in the [FAQ](./faq.md). |

For model choice, cost, chart editability, custom templates, and more, the [FAQ](./faq.md) is the place to look.
