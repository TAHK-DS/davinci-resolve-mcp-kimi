---
name: davinci-resolve
description: Control DaVinci Resolve Studio via MCP tools / Управление DaVinci Resolve Studio через MCP-инструменты. Use for any Resolve task — projects, timelines, editing, media import, bins, metadata, markers, color grading and LUTs, Fusion comps, Fairlight audio, render and export. Triggers / Триггеры: "open project", "create timeline", "render timeline", "apply LUT", DaVinci, Resolve, timeline, grading, «открой проект», «создай таймлайн», «собери нарезку», «импортируй видео в медиапул», «поставь маркер», «применяй LUT», «отрендери/экспортируй», монтаж, грейдинг, таймлайн.
---

# DaVinci Resolve (MCP)

Controls a running DaVinci Resolve Studio through the `davinci-resolve` MCP server
(37 composite tools: `project_manager`, `timeline`, `timeline_item`, `media_pool`,
`render`, `timeline_item_color`, `fusion_comp`, and more).

Управление запущенным DaVinci Resolve Studio через MCP-сервер `davinci-resolve`
(37 составных инструментов: `project_manager`, `timeline`, `timeline_item`,
`media_pool`, `render`, `timeline_item_color`, `fusion_comp` и др.).

## Prerequisites / Предусловия

1. DaVinci Resolve Studio is **running** with the target project open. /
   DaVinci Resolve Studio **запущен** и открыт нужный проект.
2. In Resolve: Preferences → General → **External scripting using: Local**. /
   В Resolve включено: Preferences → General → **External scripting using: Local**.
3. If tools answer "Resolve not running", ask the user to open Resolve — do not
   fall back to ad-hoc scripts while MCP is available. /
   Если инструменты отвечают «Resolve not running» — попроси пользователя открыть
   Resolve; не обходи MCP самодельными скриптами, пока MCP доступен.

## How to work / Как работать

- Every tool takes an `action` parameter; call a tool with `action="list_actions"`
  (or read its description) first, then invoke the concrete action with `params`. /
  У каждого инструмента есть параметр `action`; сначала вызови инструмент с
  `action="list_actions"` (или прочитай описание), затем вызывай конкретное
  действие с `params`.
- Replies come in an `_operation` envelope: `status` (success/partial/blocked/failed),
  `verification`, `changes`, `warnings`. Trust `verification`, not just `status`. /
  Ответы приходят в конверте `_operation`: `status`, `verification`, `changes`,
  `warnings`. Доверяй `verification`, а не только `status`.
- Destructive actions (delete, overwrite) require the user's explicit consent —
  show the plan first. / Разрушительные действия (удаление, перезапись) требуют
  явного согласия пользователя — сначала покажи план.
- Actions flagged as traps (e.g. `timeline_item_color.copy_grades`) may require
  `acknowledge_trap: true` — use only after warning the user. /
  Для действий-ловушек (например `timeline_item_color.copy_grades`) сервер может
  потребовать `acknowledge_trap: true` — используй только после предупреждения
  пользователя.

## Typical flows / Типовые сценарии

- "Import a folder of videos and build a timeline" / «Импортируй папку с видео и
  собери таймлайн» → `media_storage` / `media_pool` (import, bins) → `timeline`
  (create, insert clips).
- "Render the timeline to H.264" / «Отрендери таймлайн в H.264» → `render`
  (settings, validation, queue, start).
- "Apply a LUT to clips" / «Применяй LUT к клипам» → `lut` +
  `timeline_item_color` / `graph`.
- "Mark silent ranges" / «Расставь маркеры по тишине» → `media_analysis`
  (requires ffmpeg on PATH) → `timeline_markers`.

## Technical notes / Технические детали

- The server sources and its virtualenv live inside the plugin: `server/`
  (`server/venv` is created by `setup.sh` with `--copies`). /
  Исходники сервера и его venv лежат внутри плагина: `server/`
  (`server/venv` создаётся скриптом `setup.sh` с флагом `--copies`).
- Upstream server project: `davinci-resolve-mcp` (samuelgursky, MIT). /
  Апстрим сервера: `davinci-resolve-mcp` (samuelgursky, MIT).
