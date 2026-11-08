#!/usr/bin/env python3
"""CI check: plugin manifest sanity.

Validates kimi.plugin.json structure, referenced paths, and locale files —
a lightweight standalone counterpart of the local Kimi plugin validator,
so the check runs on any CI machine without the Kimi toolchain.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def fail(msg):
    errors.append(msg)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {e}")
        return None


manifest = load_json(ROOT / "kimi.plugin.json")
if manifest is not None:
    for key in ("name", "version", "description", "skills", "mcpServers", "interface"):
        if key not in manifest:
            fail(f"kimi.plugin.json: missing required key {key!r}")

    itf = manifest.get("interface", {})
    if itf.get("defaultLocale") not in ("zh-CN", "en-US"):
        fail(f"kimi.plugin.json: interface.defaultLocale must be zh-CN or en-US, got {itf.get('defaultLocale')!r}")
    prompts = itf.get("tryPrompts")
    if not (isinstance(prompts, list) and any(isinstance(p, str) and p.strip() for p in prompts)):
        fail("kimi.plugin.json: interface.tryPrompts must contain at least one non-empty prompt")

    servers = manifest.get("mcpServers", {})
    if "davinci-resolve" not in servers:
        fail("kimi.plugin.json: mcpServers is missing the 'davinci-resolve' entry")
    else:
        srv = servers["davinci-resolve"]
        for arg in srv.get("args", []):
            if arg.startswith("./") and not (ROOT / arg).exists():
                fail(f"kimi.plugin.json: mcpServers arg path does not exist: {arg}")

    skills_dir = ROOT / "skills"
    skill_md = skills_dir / "davinci-resolve" / "SKILL.md"
    if not skill_md.is_file():
        fail("skills/davinci-resolve/SKILL.md is missing")

locales_dir = ROOT / "locales"
locale_files = sorted(locales_dir.glob("*.json")) if locales_dir.is_dir() else []
if not locale_files:
    fail("locales/: no locale files found")
for lf in locale_files:
    data = load_json(lf)
    if data is None:
        continue
    if not data.get("displayName"):
        fail(f"{lf.name}: missing displayName")
    if not (isinstance(data.get("tryPrompts"), list) and any(str(p).strip() for p in data["tryPrompts"])):
        fail(f"{lf.name}: missing non-empty tryPrompts")

covered = {lf.stem for lf in locale_files} | {manifest.get("interface", {}).get("defaultLocale") if manifest else None}
for required in ("zh-CN", "en-US"):
    if required not in covered:
        fail(f"locales/ together with defaultLocale must cover {required}")

if errors:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
print(f"OK: manifest valid, {len(locale_files)} locale files, mcpServers entry present")
