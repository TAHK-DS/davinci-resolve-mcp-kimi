# DaVinci Resolve MCP — Kimi Plugin

**[Русская версия](README.ru.md)**

Control **DaVinci Resolve Studio** directly from [Kimi](https://www.kimi.com/) (Kimi Work desktop agent): projects, timelines, editing, media pool, color grading & LUTs, Fusion, Fairlight, rendering and export — **37 composite tools** over the official Resolve Scripting API, exposed as a local MCP server.

This repository is a ready-to-install **Kimi plugin** that packages the open-source [`davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp) server (MIT, by @samuelgursky — all credit for the server goes upstream) together with a Kimi skill that teaches the agent how to drive Resolve.

## What you get

| Component | Contents |
|---|---|
| MCP server `davinci-resolve` | 37 tools: `project_manager`, `timeline`, `timeline_item`, `media_pool`, `media_storage`, `render`, `render_presets`, `lut`, `timeline_item_color`, `graph`, `fusion_comp`, `media_analysis`, `resolve_control`, `setup` and more |
| Skill `davinci-resolve` | Agent instructions (EN + RU): when to trigger, action-dispatch pattern, safety rules |
| `setup.sh` | One-step environment setup (venv + dependencies) |

## Requirements

- **DaVinci Resolve Studio** (external scripting is a Studio feature; the free edition is partially reachable via the in-app bridge — see upstream docs). Tested on Resolve Studio 21.2.
- **Python 3.10+** on `PATH` (3.10–3.12 recommended).
- Kimi desktop client (Kimi Work).
- In Resolve: **Preferences → General → External scripting using: Local**.

## Installation

```bash
git clone https://github.com/TAHK-DS/davinci-resolve-mcp-kimi.git
cd davinci-resolve-mcp-kimi
bash setup.sh
```

`setup.sh` creates `server/venv` **with `--copies`** (no symlinks — Kimi's plugin safety scan rejects symlinked interpreters) and installs the Python dependencies.

Then register the plugin in Kimi:

1. Open the **Plugins** page → **Personal** tab.
2. Add the plugin from this folder (or run `register_personal.sh <this folder>` from the Kimi `plugin-builder` skill).
3. Click **＋** to install — hot reload, no restart needed.

## Usage examples

- "Create a timeline from the clips in the current bin"
- "Render the current timeline to H.264"
- "Apply the HockeyGrade LUT to every clip on the timeline"
- "Mark silent ranges and cut a highlights reel"

The Resolve application must be running (the server can also launch it on first call — up to 60 s).

## Platform notes

The bundled `kimi.plugin.json` ships **macOS** paths in `mcpServers.env` (`RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB`, `PYTHONPATH`). On other platforms adjust them:

- **Windows**: `RESOLVE_SCRIPT_API=%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`, `RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll`
- **Linux**: `RESOLVE_SCRIPT_API=/opt/resolve/Developer/Scripting`, `RESOLVE_SCRIPT_LIB=/opt/resolve/libs/Fusion/fusionscript.so`

The optional Node-based advanced offline server (`server/resolve-advanced`) is not required for the MCP tools and is not installed by `setup.sh`; see the upstream README if you need it.

## License

- Plugin wrapper (manifest, skill, setup script): **MIT**.
- Bundled server: [`davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp) by Samuel Gursky, **MIT** — see `server/LICENSE`.
