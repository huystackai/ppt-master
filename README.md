# PPT Master — a portable AI Agent skill

English | [中文](README_CN.md)

Create natively editable PowerPoint presentations from documents, web sources, spreadsheets, text, or a topic. The complete skill lives in this directory: `SKILL.md`, scripts, role references, workflows, templates, icons, charts, documentation, and example projects.

## Install

Copy this entire folder into your agent's skills directory and name it **`ppt-master`**. `SKILL.md` must be directly inside `ppt-master/`. You can also clone your published repository directly into that location and use `git pull --ff-only` for updates.

```text
<agent-skills-directory>/
└── ppt-master/
    ├── SKILL.md
    ├── agents/
    ├── scripts/
    ├── references/
    ├── workflows/
    ├── templates/
    ├── docs/
    ├── examples/
    ├── requirements.txt
    └── LICENSE
```

Use an agent that supports local skills, reading/writing files, and shell commands. Python 3.10+ must be available. On first use, the agent runs `scripts/bootstrap.py` to install Python dependencies in a user-cache virtual environment and uses the returned interpreter automatically. No manual pip installation or environment activation is required. The first setup needs network access; later runs reuse the environment.

For agents without automatic skill discovery, tell the agent to read this folder's `SKILL.md` before handling the presentation. The optional Claude plugin metadata also loads this root skill; it does not fetch a different upstream version.

## Use

Attach your content and ask, for example:

> Use ppt-master to create an editable 12-slide presentation from this report.

To follow a sample, attach the sample and say:

> Use this PPTX as the design reference and this report for the content.

PDF pages and slide screenshots also work as samples. **Times New Roman** is the default for ordinary slide text. You can request another font or preserve the sample's typography.

The agent confirms the design plan, prepares the deck, opens live preview, and exports editable PPTX. Projects and outputs go into your current workspace, separate from the installed skill. The agent uses absolute skill paths, so installation directories containing spaces work.

## Full feature set

| Capability | Included |
|---|---|
| Source conversion | PDF, Word/DOCX, Excel, PowerPoint, EPUB, HTML, Markdown, URLs, and legacy formats through their existing fallback tools |
| Topic research | Web research and source collection when no substantive input is provided |
| Templates and branding | Layout, brand and deck libraries; fusion; reusable template creation and registration |
| Uploaded samples | Follow PPTX, PDF, SVG, or slide screenshots while producing editable output |
| Images | Every existing AI image backend, web image sourcing, manifests, image analysis and processing |
| Visualization | Chart library, diagrams, infographics and chart-coordinate verification |
| Formulas | LaTeX rendering with the existing provider fallback chain |
| Preview and editing | Live browser preview, annotations, text/style editing, dragging, keyboard nudging and re-export |
| PPTX export | Native DrawingML shapes/text, SVG snapshot option, notes and optional paragraph merging |
| Motion | Slide transitions, entrance animations and custom object-level animation controls |
| Audio and video | Narration, recorded timings, provider voices, supported voice cloning and video workflow |
| Review | SVG checks and optional per-page visual review, with serial fallback on agents without delegation |
| Continuation | Split-mode execution and resumption from saved project state |
| Example gallery | Complete bundled example decks and the static browser viewer |

All original tools and bundled resource libraries are retained. The skill uses your agent's available tools rather than requiring a particular model or vendor.

## Optional provider configuration

API credentials are needed only for the provider features you choose. Copy `.env.example` to `.env` in your working directory or configure your process environment; `~/.ppt-master/.env` is also supported. The agent asks for missing configuration when that feature is used. The example file contains no configured credentials.

Some paths use external tools: Pandoc for legacy document formats, FFmpeg for video, and Chromium/OS browser libraries for visual review. The agent prepares Chromium through `bootstrap.py --browser` when review is requested and reports any remaining system requirement. These features remain available; their prerequisites are not silently skipped.

## Guides and maintenance

- [Agent workflow](SKILL.md)
- [Getting started](docs/getting-started.md)
- [Uploaded slide samples](workflows/use-slide-reference.md)
- [Templates guide](docs/templates-guide.md)
- [Scripts and tools](scripts/README.md)
- [Troubleshooting](docs/faq.md)

To check the runtime without installing anything:

```bash
python3 scripts/bootstrap.py --check
```

To prepare it manually if needed:

```bash
python3 scripts/bootstrap.py
```

Use the absolute Python path in the JSON response for later commands. On Windows, use `python` or `py -3` if `python3` is unavailable.

Maintainers can run `python3 scripts/package_skill.py` to build a complete shareable skill ZIP. It includes the full feature set and example gallery, while excluding Git history, actual `.env` files, user projects, virtual environments and caches.

## License and attribution

Based on [PPT Master by Hugo He](https://github.com/hugohe3/ppt-master), licensed under [MIT](LICENSE). The original copyright notice is retained. Bundled icon libraries retain their existing attribution and license documentation.
