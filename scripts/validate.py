#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "shadowrocket-dd.conf"
WEATHERKIT_MODULE = ROOT / "modules" / "iRingo.WeatherKit.srmodule"
MAPKIT_MODULE = ROOT / "modules" / "iRingo.MapKit.srmodule"

text = CONF.read_text(encoding="utf-8")
lines = text.splitlines()
errors = []

required_sections = ["[General]", "[Proxy]", "[Proxy Group]", "[Rule]", "[Host]"]
for section in required_sections:
    if section not in text:
        errors.append(f"missing section: {section}")

# Parse sections.
section = None
groups = {}
rule_lines = []
proxy_active_lines = []
for lineno, raw in enumerate(lines, 1):
    s = raw.strip()
    if not s or s.startswith("#"):
        continue
    if s.startswith("[") and s.endswith("]"):
        section = s
        continue
    if section == "[Proxy Group]" and " = " in s:
        name = s.split(" = ", 1)[0].strip()
        if name in groups:
            errors.append(f"duplicate proxy group '{name}' at lines {groups[name]} and {lineno}")
        groups[name] = lineno
    elif section == "[Rule]":
        rule_lines.append((lineno, s))
    elif section == "[Proxy]":
        proxy_active_lines.append((lineno, s))

# Public repo safety: [Proxy] must stay empty; real subscriptions live only in Shadowrocket.
if proxy_active_lines:
    for lineno, s in proxy_active_lines:
        errors.append(f"[Proxy] must remain empty in public repo (line {lineno}: {s})")

required_groups = {
    "☁️ 白月光优选",
    "🅱️ BoostNet优选",
    "⚡ 双机场自动",
    "🛟 双机场容灾",
    "🚀 主节点",
    "🤖 AI固定美国节点",
    "🤖 AI服务",
    "🛡 广告拦截",
    "🔒 国内网络",
    "🐟 漏网之鱼",
}
for name in sorted(required_groups):
    if name not in groups:
        errors.append(f"missing required proxy group: {name}")

# Exact Shadowrocket subscription display names required by use=true.
for needle in ("白月光,use=true", "BoostNet,use=true"):
    if needle not in text:
        errors.append(f"missing subscription selector: {needle}")

# Validate policies referenced by active rules.
builtins = {"DIRECT", "REJECT", "PROXY"}
for lineno, s in rule_lines:
    parts = [p.strip() for p in s.split(",")]
    if len(parts) < 2:
        errors.append(f"malformed rule at line {lineno}: {s}")
        continue

    rule_type = parts[0]
    if rule_type == "FINAL":
        policy = parts[1]
    elif len(parts) >= 3:
        policy = parts[2]
    else:
        errors.append(f"cannot determine policy at line {lineno}: {s}")
        continue

    if policy not in builtins and policy not in groups:
        errors.append(f"unknown policy '{policy}' referenced at line {lineno}")

# Maintenance contract.
expected_update = "update-url = https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/shadowrocket-dd.conf"
if expected_update not in text:
    errors.append("update-url does not point to the canonical main-branch config")

# Optional WeatherKit module must remain self-hosted, narrowly scoped and compatible with the main policy names.
if not WEATHERKIT_MODULE.exists():
    errors.append("missing WeatherKit module: modules/iRingo.WeatherKit.srmodule")
else:
    module_text = WEATHERKIT_MODULE.read_text(encoding="utf-8")
    required_module_strings = [
        "#!url = https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/modules/iRingo.WeatherKit.srmodule",
        "#!arguments = endpoint:weatherkit.pages.dev",
        "[Rule]",
        "DOMAIN,weatherkit.apple.com,🚀 主节点",
        "DOMAIN,weatherkit.pages.dev,DIRECT",
        "DOMAIN,weather.nanocat.cloud,🚀 主节点",
        "[URL Rewrite]",
        "https://{{{endpoint}}}/api/v1/availability/",
        "https://{{{endpoint}}}/api/v2/weather/",
        "[MITM]",
        "hostname = %APPEND% weatherkit.apple.com",
    ]
    for needle in required_module_strings:
        if needle not in module_text:
            errors.append(f"WeatherKit module missing required content: {needle}")

    if "🚀 主节点" not in groups:
        errors.append("WeatherKit module requires missing proxy group: 🚀 主节点")


# Optional MapKit module must remain self-hosted and use the upstream Rewrite module's narrow MITM scope.
if not MAPKIT_MODULE.exists():
    errors.append("missing MapKit module: modules/iRingo.MapKit.srmodule")
else:
    module_text = MAPKIT_MODULE.read_text(encoding="utf-8")
    required_module_strings = [
        "#!url = https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/modules/iRingo.MapKit.srmodule",
        "#!arguments = endpoint:mapkit.pages.dev",
        "[Rule]",
        "DOMAIN-SUFFIX,is.autonavi.com,DIRECT",
        "[URL Rewrite]",
        "https://{{{endpoint}}}/config/defaults",
        "https://{{{endpoint}}}/config/announcements",
        "https://{{{endpoint}}}/geo_manifest/dynamic/config",
        "[MITM]",
        "hostname = %APPEND% configuration.ls.apple.com, gspe35-ssl.ls.apple.com",
    ]
    for needle in required_module_strings:
        if needle not in module_text:
            errors.append(f"MapKit module missing required content: {needle}")

if errors:
    print("Shadowrocket config validation FAILED:\n")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print(
    "Shadowrocket config validation PASS: "
    f"{len(groups)} proxy groups, {len(rule_lines)} active rules, WeatherKit and MapKit modules OK"
)
