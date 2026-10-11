# PPT Master — 可直接安装的 AI Agent Skill

[English](README.md) | 中文

将文档、网页、表格、文字或主题制作成原生可编辑的 PowerPoint。这个文件夹就是完整 skill，包含 `SKILL.md`、脚本、角色说明、工作流、模板、图标、图表、文档和全部示例。

## 安装

将**整个文件夹**复制到 Agent 的 skills 目录，文件夹命名为 `ppt-master`，确保 `SKILL.md` 直接位于其中。也可以将你发布的仓库直接 clone 到该位置，以后通过 `git pull --ff-only` 更新。

```text
<Agent 的 skills 目录>/
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

Agent 需要支持本地 skill、文件读写和 shell 命令。系统需有 Python 3.10+。首次使用时，Agent 自动运行 `scripts/bootstrap.py`，在用户缓存目录创建环境并安装依赖，之后使用返回的 Python 解释器。无需手动运行 pip 或激活虚拟环境。首次安装需要联网，后续会复用环境。

如果 Agent 不会自动发现 skill，请让它先读取本目录的 `SKILL.md`。附带的 Claude 插件配置也加载这个根目录 skill，不会下载其他版本。

## 使用

上传内容资料后说：

> 用 ppt-master 把这份报告做成 12 页可编辑的 PPT。

需要按样稿制作时，上传样稿并说明：

> 这个 PPTX 是设计样稿，这份报告是内容，请按样稿制作。

也支持 PDF 页面、SVG 或幻灯片截图。普通文本默认使用 **Times New Roman**；你可以要求其他字体，或保留样稿字体。

Agent 会确认设计方案、生成页面、打开实时预览并导出可编辑 PPTX。项目和产物保存在当前工作目录，skill 安装目录只保存工具和资源。包含空格的安装路径也受支持。

## 完整功能

| 能力 | 保留内容 |
|---|---|
| 来源转换 | PDF、Word/DOCX、Excel、PowerPoint、EPUB、HTML、Markdown、URL，以及通过原有工具处理的旧格式 |
| 主题研究 | 无实质来源时的网页研究与资料收集 |
| 模板和品牌 | 版式、品牌、完整 deck 库；融合；模板创建与注册 |
| 上传样稿 | 参考 PPTX、PDF、SVG、截图，生成可编辑新 deck |
| 图片 | 全部原有 AI 生图后端、网页图片、清单、分析和处理工具 |
| 图表与公式 | 图表库、图解、信息图、坐标校验，以及 LaTeX 渲染回退链 |
| 预览与编辑 | 实时预览、注解、文本与样式修改、拖动、键盘微调、重新导出 |
| PPTX 导出 | 原生 DrawingML、SVG 快照、演讲者备注、可选段落合并 |
| 动画 | 页间转场、入场动画、对象级顺序、效果和时序定制 |
| 音视频 | 旁白、录制时序、provider 音色、声音复刻和视频工作流 |
| 检查 | SVG 检查、按需逐页视觉检查；不支持子 Agent 时可串行执行 |
| 续作 | 分阶段执行与项目恢复 |
| 示例 | 全部示例 deck 和静态浏览器查看器 |

保留全部原有脚本与资源库，使用宿主 Agent 可用的工具，不绑定指定厂商或模型。

## 按需配置

只有使用某个云端 provider 时才需要它的凭据。将 `.env.example` 复制为工作目录里的 `.env`，或使用环境变量；也支持 `~/.ppt-master/.env`。示例文件没有配置真实密钥。

部分功能按需使用系统工具：旧文档格式使用 Pandoc，视频使用 FFmpeg，视觉检查使用 Chromium 和系统浏览器库。Agent 在需要时运行 `bootstrap.py --browser`，并说明尚缺的系统依赖。

## 文档与维护

- [Agent 工作流](SKILL.md)
- [快速入门](docs/zh/getting-started.md)
- [参考幻灯片](workflows/use-slide-reference.md)
- [模板指南](docs/zh/templates-guide.md)
- [脚本工具](scripts/README.md)
- [常见问题](docs/zh/faq.md)

只检查环境而不安装：`python3 scripts/bootstrap.py --check`。手动准备环境：`python3 scripts/bootstrap.py`。后续命令使用 JSON 中返回的 Python 绝对路径；Windows 没有 `python3` 时可用 `python` 或 `py -3`。

维护者运行 `python3 scripts/package_skill.py` 即可构建完整的共享 ZIP，包含全部功能和示例，排除 Git 历史、真实 `.env`、私人项目、虚拟环境和缓存。

## 许可与来源

基于 [Hugo He 的 PPT Master](https://github.com/hugohe3/ppt-master)，遵循 [MIT 许可](LICENSE)，保留原始版权声明。图标库保留各自的许可和来源说明。
