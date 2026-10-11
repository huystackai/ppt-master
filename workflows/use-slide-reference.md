---
description: Follow an uploaded or drag-and-drop slide sample for the current presentation without registering a global template.
---

# Use an Uploaded Slide Reference

Run at SKILL.md Step 3 when the user attaches a sample and asks to follow it, or supplies a reference file path. Examples: "làm slide theo mẫu này", "use this deck as the template", or "match these slide screenshots".

This workflow uses the chat client's existing attachment support. It does not add an upload interface to the live-preview editor. Use the attachment's accessible local path; if the file cannot be accessed, ask the user to attach it again or supply a readable path.

## Step 1: Preserve and classify the sample

Copy each original into `<project_path>/sources/slide-references/<reference_id>/`, using stable IDs such as `reference_01`. Preserve original filenames and the user's intended page order. Do not move or overwrite the originals. Keep content sources separate; sample text and data are not factual source material unless the user explicitly requests their reuse.

| Input | Preparation | Fidelity |
|---|---|---|
| `.pptx` | Run the existing importer below; inspect metadata and slide geometry | Extracted fonts, colors, dimensions, and layouts; report unsupported objects |
| `.pdf` | Render the supplied pages to PNG using an available PDF renderer; visually inspect each page | Layout and color estimates; font names only when supported by extracted metadata |
| `.png`, `.jpg`, `.jpeg` | Visually inspect every supplied slide screenshot | Layout and style estimates; do not claim exact font identification |
| `.svg` | Read SVG geometry/styles, resolve linked assets, and visually inspect a rendering | Extracted geometry, colors, and declared fonts |
| `.ppt`, `.potx`, or unreadable file | Ask for a `.pptx`, PDF, or screenshots | Do not silently treat an unsupported file as imported |

For PPTX, run against the preserved copy:

```bash
python3 "${SKILL_DIR}/scripts/pptx_template_import.py" "<reference_copy.pptx>" -o "<reference_dir>/import"
```

Read `manifest.json`, all `svg/master_*.svg`, all `svg/layout_*.svg`, `svg/inheritance.json`, then the supplied slides' `svg/slide_*.svg`. Inspect the corresponding `svg-flat/slide_*.svg` renderings for the complete composition. Keep the workspace and extracted assets together so relative image paths resolve. Do not generate final project slides during this preparation.

For PDF, one available command is:

```bash
pdftoppm -png -r 120 "<reference_copy.pdf>" "<reference_dir>/page"
```

If the preferred renderer is unavailable, use an available equivalent. Inspect the resulting pages with an image-viewing tool; Markdown text extraction alone does not establish the slide's design. This visual inspection is an explicit exception to SKILL.md's ordinary content-image handling rule.

## Step 2: Save the reference analysis

Write `<project_path>/sources/slide-references/reference_analysis.md`. Distinguish extracted facts from visual estimates. Include:

| Item | Record |
|---|---|
| Inventory | Original filenames, reference IDs, page numbers, local reference/rendering paths, inspected pages |
| Canvas | Aspect ratio and dimensions; use the sample's aspect ratio unless the user chooses another |
| Visual system | Backgrounds, palette, title positions, margins, columns, spacing, decorative motifs, header/footer, page numbering |
| Typography | Extracted or estimated source typography separately from the proposed output font: Times New Roman by default |
| Page types | Cover, agenda, chapter, content, chart/table, closing; describe each distinct layout and its capacity |
| Assets | Reusable logos/backgrounds and their paths; identify sample-only images that should be replaced |
| Limits | Unsupported objects, unreadable labels, missing assets, and pages with uncertain reconstruction |

Use the provided layout for corresponding page types. A single screenshot defines only the demonstrated layout; infer other page types from its visual system and label that choice as an adaptation. For several samples, preserve the requested order and record which sample controls each page type. If they conflict and no priority is supplied, ask which one should control the conflicting design choice.

**Default font**: keep Times New Roman in generated text, even if the sample uses another family. If the user asks to preserve the sample's typography, use the extracted font or propose a named substitute when it cannot be identified. Confirm this within item 7 of the existing Eight Confirmations; do not add a separate template-creation gate.

## Step 3: Hand off to Strategist

Return to SKILL.md Step 4. Read the saved analysis before composing the Eight Confirmations. Present the proposed sample-derived canvas, palette, layouts, asset reuse, font policy, and reconstruction limits in the relevant confirmation items.

After confirmation, carry the following into the project `design_spec.md`:

- Section III/V: reference paths and the visual elements to preserve or adapt.
- Section IV: resolved output font stacks, using the skill's default/override precedence.
- Section VIII: each reused image asset, copied into project `images/`, with its actual path.
- Section IX: for every reference-guided output page, declare **Reference source**, **Reference page**, **Preserve**, and **Adapt**. Use project-relative paths and explicit source page numbers so a fresh Phase B session can recover the mapping.

Populate `spec_lock.md` with the confirmed colors, fonts, images, and rhythm. `page_layouts` remains reserved for actual template SVGs selected through the directory flow; do not put screenshot paths, PDF pages, or unregistered importer paths there. Reference-only pages are guided by Section IX even when `page_layouts` is absent.

Do not write to the global template library or register an index entry. If the user explicitly requests a reusable library template, route to [`create-template.md`](./create-template.md) instead.

## Step 4: Executor handoff and validation

Executor reads the Section IX reference mapping and saved analysis before the first output slide. Batch-load each referenced SVG or rendered sample once. Declare the chosen sample/page alongside the normal page-template mapping, then write each final page sequentially under the existing Step 6 rules.

Rebuild text, tables, charts, and diagrams as editable SVG elements for native PPTX export. Preserve the sample's composition and decorative language while replacing example content with the user's content. Whole-slide screenshots are references, not finished slide backgrounds. Actual logos, photos, and decorative backgrounds may remain image assets. Recreate unsupported imported chart/SmartArt placeholders from the user's content; do not pass importer badges or placeholder boxes into the final deck.

When Times New Roman or longer replacement text changes line lengths, adjust wrapping, font size within the confirmed ramp, and spacing to avoid overflow. Split an overfull page or select a better-fitting sample layout; do not drop factual content merely to match the sample. Record any material layout adaptation in Section IX.

Verify the mapped source paths exist, reused assets resolve, and generated text uses the confirmed font. Continue with the normal quality checker, post-processing, and PPTX export. Per-page visual review remains opt-in under the existing `visual-review` trigger.
