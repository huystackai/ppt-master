# AGENTS.md

This file is the project entry point for general AI agents.

The repository root is also the installable `ppt-master` skill directory. Start with SKILL.md's Portable Agent Setup, use its resolved absolute resource paths and cached Python interpreter, and write project files in the user's workspace.

**You MUST read [`SKILL.md`](SKILL.md) before any PPT generation task or repo modification.** This repository exists to generate presentations; SKILL.md is the authoritative workflow that owns project creation, role switching, serial execution, quality gates, post-processing, export, and every per-step command. The rest of this file only points to where related material lives — it never substitutes for SKILL.md.

## Project Overview

PPT Master is an AI-driven presentation generation system. Multi-role collaboration (Strategist → Image_Generator → Executor) converts source documents (PDF/DOCX/URL/Markdown) into natively editable PPTX with real PowerPoint shapes (DrawingML).

**Core Pipeline**: `Source Document → Create Project → [Template] → Strategist Eight Confirmations → [Image_Generator] → Executor Live Preview → Quality Check → Post-processing → Export PPTX`

> Topic-only requests with no source material: run the standalone [`topic-research`](workflows/topic-research.md) workflow before SKILL.md Step 1 to gather web materials.
>
> Phase B resumption (split-mode execution): when the user opens a fresh chat and says "继续生成 projects/<x>" or similar, run the standalone [`resume-execute`](workflows/resume-execute.md) workflow to enter Phase B (SVG generation + export) without re-running Phase A.
>
> Decks containing data charts: run the standalone [`verify-charts`](workflows/verify-charts.md) workflow between the executor and post-processing steps to calibrate chart coordinates.
>
> Recorded narration / video export: run the standalone [`generate-audio`](workflows/generate-audio.md) workflow after post-processing.
>
> Object-level animation tuning: when the user asks to change animation order, effect, timing, or a specific object's reveal behavior, run the standalone [`customize-animations`](workflows/customize-animations.md) workflow. Default export already has global animations; do not create `animations.json` unless customization was requested.
>
> Live preview: any time the user mentions "live preview", "preview", "看效果", or wants to click/select a slide element, run [`live-preview`](workflows/live-preview.md). Step 6 auto-starts it during generation; the workflow covers post-export re-entry and applying submitted annotations.
>
> Uploaded slide samples: when the user drags a PPTX, PDF, or slide image into chat and asks to follow it, run [`use-slide-reference`](workflows/use-slide-reference.md) at Step 3. Keep the sample separate from factual content sources; preserve Times New Roman as the default unless overridden. This is project-level reference use, not global template or brand creation.
>
> Brand identity setup: when the user asks to "set up brand" / "建立品牌" / "做品牌规范", provides a brand asset for identity setup (logo / brand site URL / branded PPTX / brand PDF), or wants to extract a brand from existing materials, run the standalone [`create-brand`](workflows/create-brand.md) workflow. Output goes to `templates/brands/<id>/`. Brands apply at SKILL.md Step 3 via the explicit brand-directory path rule; bare brand names never trigger. A branded slide sample supplied only to guide the current deck follows `use-slide-reference` instead.
>
> Visual self-check: only when the user explicitly requests a per-page visual review on the generated SVGs (e.g., "跑一下视觉自检 / 视觉回看 / 视觉 rubric", "visual review", "check each page visually"), run the standalone [`visual-review`](workflows/visual-review.md) workflow between the executor and post-processing steps. The main pipeline does NOT invoke it automatically; do not infer or recommend it from deck size, model identity, or any other signal — user request is the only trigger.

## Execution Requirements

- For standalone template creation (no source deck), read [`workflows/create-template.md`](workflows/create-template.md).
- Technical SVG/PPT constraints live in [`references/shared-standards.md`](references/shared-standards.md).
- Canvas choices live in [`references/canvas-formats.md`](references/canvas-formats.md).
- Icon library details live in [`templates/icons/README.md`](templates/icons/README.md).

## Required Conventions

- **Repo-wide style rules** — when editing prompt files under [`references/`](references/), Python under [`scripts/`](scripts/), or any other code/prose in the repo, follow the matching style rule in [`docs/rules/`](docs/rules/).
- **Markdown language consistency** — Markdown files under `workflows/`, `references/`, and `docs/` are currently single-language per directory. New files mirror the language of their siblings; do not mix English scaffolding with Chinese paragraphs (or vice versa) inside one file. Chat replies are unaffected.

## Compatibility Boundary

- This repository is a workflow/skill package, not an app or service scaffold.
- Do NOT assume generic-project conventions like `.worktrees/`, `tests/`, or mandatory branch setup unless the user explicitly requests them.
- On conflict with a generic coding skill, prioritize [`SKILL.md`](SKILL.md) inside this repository.

## Command Quick Reference

Convenience summary only — full workflow in [`SKILL.md`](SKILL.md).

```bash
# Source content conversion
python3 "${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py" <PDF_file>
python3 "${SKILL_DIR}/scripts/source_to_md/doc_to_md.py" <DOCX_or_other_file>
python3 "${SKILL_DIR}/scripts/source_to_md/excel_to_md.py" <XLSX_or_XLSM_file>
python3 "${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py" <PPTX_file>
python3 "${SKILL_DIR}/scripts/source_to_md/web_to_md.py" <URL>

# Project management
python3 "${SKILL_DIR}/scripts/project_manager.py" init <project_name> --format ppt169
python3 "${SKILL_DIR}/scripts/project_manager.py" import-sources <project_path> <source_files_or_URLs...> --move
python3 "${SKILL_DIR}/scripts/project_manager.py" validate <project_path>

# Image tools and SVG quality check
python3 "${SKILL_DIR}/scripts/analyze_images.py" <project_path>/images
# In-pipeline AI image generation — manifest mode (required, even for 1 image):
python3 "${SKILL_DIR}/scripts/image_gen.py" --manifest <project_path>/images/image_prompts.json
python3 "${SKILL_DIR}/scripts/image_gen.py" --render-md <project_path>/images/image_prompts.json
# Out-of-pipeline one-off / debug / single-image fixup only (no manifest, no sidecar):
python3 "${SKILL_DIR}/scripts/image_gen.py" "prompt" --aspect_ratio 16:9 --image_size 1K -o <project_path>/images
python3 "${SKILL_DIR}/scripts/svg_editor/server.py" <project_path> --live
python3 "${SKILL_DIR}/scripts/svg_quality_checker.py" <project_path>
python3 "${SKILL_DIR}/scripts/animation_config.py" scaffold <project_path>  # optional, only for custom object-level animation
python3 "${SKILL_DIR}/scripts/animation_config.py" validate <project_path>  # optional, before re-export

# Post-processing pipeline: run sequentially, one command at a time
python3 "${SKILL_DIR}/scripts/total_md_split.py" <project_path>
python3 "${SKILL_DIR}/scripts/finalize_svg.py" <project_path>
python3 "${SKILL_DIR}/scripts/svg_to_pptx.py" <project_path>
# Add --merge-paragraphs when the user wants paragraph-level editable text frames instead of one-per-line (default off, see SKILL.md Step 7.3).
```

## Core Directories

- `SKILL.md` — main workflow authority.
- `references/` — role definitions and technical specifications.
- `scripts/` — runnable tool scripts.
- `scripts/docs/` — topic-focused script docs.
- `templates/` — layout templates, chart templates, icon library, brand presets.
- `workflows/` — standalone workflow files.
- `docs/` — user-facing documentation (FAQ, installation, technical design, templates guide, audio narration).
- `docs/rules/` — repo-wide style rules.
- `examples/` — example projects.
- `projects/` — user project workspace.
