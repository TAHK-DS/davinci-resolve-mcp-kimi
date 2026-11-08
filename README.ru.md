# DaVinci Resolve MCP — плагин для Kimi

**[English version](README.md)**

Управление **DaVinci Resolve Studio** прямо из [Kimi](https://www.kimi.com/) (десктоп-агент Kimi Work): проекты, таймлайны, монтаж, медиапул, цветокоррекция и LUT, Fusion, Fairlight, рендер и экспорт — **37 составных инструментов** поверх официального Scripting API Resolve, доступных как локальный MCP-сервер.

Репозиторий — это готовый к установке **плагин Kimi**, в который упакован открытый MCP-сервер [`davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp) (MIT, автор @samuelgursky — вся заслуга за сервер принадлежит апстриму) и Kimi-скилл, обучающий агента работе с Resolve.

## Что внутри

| Компонент | Содержимое |
|---|---|
| MCP-сервер `davinci-resolve` | 37 инструментов: `project_manager`, `timeline`, `timeline_item`, `media_pool`, `media_storage`, `render`, `render_presets`, `lut`, `timeline_item_color`, `graph`, `fusion_comp`, `media_analysis`, `resolve_control`, `setup` и другие |
| Скилл `davinci-resolve` | Инструкции для агента (RU + EN): когда срабатывать, паттерн вызова действий, правила безопасности |
| `setup.sh` | Установка окружения в один шаг (venv + зависимости) |

## Требования

- **DaVinci Resolve Studio** (внешний скриптинг — функция Studio; бесплатная версия частично доступна через встроенный мост — см. документацию апстрима). Проверено на Resolve Studio 21.2.
- **Python 3.10+** в `PATH` (рекомендуется 3.10–3.12).
- Десктопный клиент Kimi (Kimi Work).
- В Resolve: **Preferences → General → External scripting using: Local**.

## Установка

```bash
git clone https://github.com/TAHK-DS/davinci-resolve-mcp-kimi.git
cd davinci-resolve-mcp-kimi
bash setup.sh
```

`setup.sh` создаёт `server/venv` **с флагом `--copies`** (без симлинков — проверка безопасности Kimi отклоняет интерпретаторы-симлинки) и устанавливает зависимости.

Затем зарегистрируйте плагин в Kimi:

1. Откройте страницу **Плагины** → вкладка **Personal**.
2. Добавьте плагин из этой папки (или выполните `register_personal.sh <эта папка>` из скилла `plugin-builder`).
3. Нажмите **＋** для установки — горячая перезагрузка, перезапуск не нужен.

## Примеры запросов

- «Создай таймлайн из клипов в текущем бине»
- «Отрендери текущий таймлайн в H.264»
- «Примени LUT HockeyGrade ко всем клипам на таймлайне»
- «Расставь маркеры по тишине и собери нарезку лучших моментов»

Resolve должен быть запущен (сервер может запустить его сам при первом вызове — до 60 секунд).

## Платформы

В `kimi.plugin.json` прописаны **macOS**-пути в `mcpServers.env` (`RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB`, `PYTHONPATH`). На других платформах поправьте их:

- **Windows**: `RESOLVE_SCRIPT_API=%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`, `RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll`
- **Linux**: `RESOLVE_SCRIPT_API=/opt/resolve/Developer/Scripting`, `RESOLVE_SCRIPT_LIB=/opt/resolve/libs/Fusion/fusionscript.so`

Опциональный Node-сервер расширенной офлайн-аналитики (`server/resolve-advanced`) для работы MCP-инструментов не нужен и скриптом `setup.sh` не устанавливается; см. README апстрима, если он вам требуется.

## Лицензия

- Обёртка плагина (манифест, скилл, setup.sh): **MIT**.
- Встроенный сервер: [`davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp), автор Samuel Gursky, **MIT** — см. `server/LICENSE`.
