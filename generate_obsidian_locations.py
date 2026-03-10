"""
Sword Coast Location Notes Generator for Obsidian

Reads sword_coast_locations.json and creates/updates one note per location
in the vault's Locations folder, with minimal frontmatter (map_quadrant, region,
wiki_link, color as tag), optional ## Description body, and one index file per
cardinal direction (North West.md, North.md, etc.).

Usage:
  1. Copy config.example.json to config.json and set vault_path and json_path.
  2. Export sword_coast_locations.json from AideDD (see docs/export-map.md).
  3. Run: python generate_obsidian_locations.py
"""

import json
import re
from pathlib import Path
from urllib.parse import quote

import requests

# =============================================================================
# Load config from config.json if present; otherwise use defaults below
# =============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.json"

def _load_config():
    defaults = {
        "vault_path": "",
        "json_path": "",
        "overwrite_existing": False,
        "include_descriptions": True,
        "generate_indices": True,
        "update_wiki_links": True,
    }
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                loaded = json.load(f)
            defaults.update(loaded)
        except (json.JSONDecodeError, IOError):
            pass
    return defaults

_cfg = _load_config()

VAULT = Path(_cfg["vault_path"]) if _cfg.get("vault_path") else SCRIPT_DIR
LOCATIONS_DIR = VAULT / "Locations"
JSON_PATH = Path(_cfg["json_path"]) if _cfg.get("json_path") else SCRIPT_DIR / "sword_coast_locations.json"
WIKIFAILS_PATH = VAULT / "~WikiFails~.md"
OVERWRITE_EXISTING = _cfg.get("overwrite_existing", False)
INCLUDE_DESCRIPTIONS = _cfg.get("include_descriptions", True)
GENERATE_INDICES = _cfg.get("generate_indices", True)
UPDATE_WIKI_LINKS = _cfg.get("update_wiki_links", True)

QUADRANT_LABELS = {
    "NW": "North West",
    "N": "North",
    "NE": "North East",
    "E": "East",
    "SE": "South East",
    "S": "South",
    "SW": "South West",
    "W": "West",
}

# =============================================================================
# Constants
# =============================================================================
TYPE_MAP = {
    "Area": "region",
    "Forest": "forest",
    "Mountainous": "mountain",
    "Place": "place",
    "Water": "water",
    "Road": "road",
    "Unknown": "other",
}
MAP_LINK_BASE = "https://www.aidedd.org/atlas/sword-coast"
BASE_WIKI_PAGE = "https://forgottenrealms.fandom.com/wiki/"
WIKI_API = "https://forgottenrealms.fandom.com/api.php"


def safe_filename(name: str) -> str:
    forbidden = '<>:"/\\|?*'
    for ch in forbidden:
        name = name.replace(ch, " ")
    return name.strip()


def html_to_plain(html: str) -> str:
    if not html or not html.strip():
        return ""
    text = html.replace("</p>", "\n\n").replace("<p>", "\n\n")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_quadrant(x: float, y: float, min_x: float, max_x: float, min_y: float, max_y: float) -> str:
    if max_x <= min_x or max_y <= min_y:
        return "N"
    x_norm = (x - min_x) / (max_x - min_x)
    y_norm = (y - min_y) / (max_y - min_y)
    row = 0 if y_norm < 1/3 else (1 if y_norm < 2/3 else 2)
    col = 0 if x_norm < 1/3 else (1 if x_norm < 2/3 else 2)
    if row == 0 and col == 0: return "NW"
    if row == 0 and col == 1: return "N"
    if row == 0 and col == 2: return "NE"
    if row == 1 and col == 0: return "W"
    if row == 1 and col == 2: return "E"
    if row == 2 and col == 0: return "SW"
    if row == 2 and col == 1: return "S"
    if row == 2 and col == 2: return "SE"
    return "N"


def get_region(x: float, y: float, min_x: float, max_x: float, min_y: float, max_y: float) -> str:
    if max_x <= min_x or max_y <= min_y:
        return "Sword Coast North"
    x_norm = (x - min_x) / (max_x - min_x)
    y_norm = (y - min_y) / (max_y - min_y)
    if x_norm < 0.5 and y_norm < 0.5:
        return "Sword Coast North"
    if x_norm < 0.5 and y_norm >= 0.5:
        return "Western Heartlands"
    if x_norm >= 0.5 and y_norm < 0.5:
        return "Interior North"
    return "Dalelands"


def color_to_tag(color: str) -> str:
    c = (color or "").strip().lstrip("#").lower()
    if not c:
        return "color-unknown"
    return f"color-{c}"


def guess_wiki_link(name: str) -> str:
    title = name.replace(" ", "_")
    direct_url = BASE_WIKI_PAGE + quote(title)
    try:
        resp = requests.get(direct_url, timeout=10)
        if resp.status_code < 400:
            return resp.url
    except Exception:
        pass
    try:
        params = {"action": "opensearch", "search": name, "limit": 1, "namespace": 0, "format": "json"}
        resp = requests.get(WIKI_API, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) >= 4 and data[3]:
                return data[3][0]
    except Exception:
        pass
    return ""


def build_frontmatter(loc: dict, wiki_link: str, map_quadrant: str, region: str) -> str:
    name = loc["name"]
    raw_type = loc.get("type")
    loc_type = TYPE_MAP.get(raw_type, "other")
    color_tag = color_to_tag(loc.get("color") or "")
    tags = ["location", "sword-coast", loc_type, color_tag]
    lines = [
        "---",
        f'name: "{name}"',
        f'type: "{loc_type}"',
        f'region: "{region}"',
        f'map_quadrant: "{map_quadrant}"',
        f'map_link: "{MAP_LINK_BASE}"',
        f'wiki_link: "{wiki_link}"',
        "tags:",
    ]
    for t in tags:
        lines.append(f"  - {t}")
    lines.append("---")
    return "\n".join(lines)


def build_body(description: str) -> str:
    if not INCLUDE_DESCRIPTIONS or not description:
        return ""
    plain = html_to_plain(description)
    if not plain:
        return ""
    return "## Description\n\n" + plain + "\n"


def write_note(path: Path, loc: dict, wiki_link: str, map_quadrant: str, region: str) -> bool:
    name = loc["name"]
    body = build_body(loc.get("description") or "")
    fm = build_frontmatter(loc, wiki_link, map_quadrant, region)
    content = fm + "\n" + body if body else fm + "\n"

    if path.exists() and not OVERWRITE_EXISTING:
        text = path.read_text(encoding="utf-8")
        if "---" in text:
            parts = text.split("---", 2)
            if len(parts) >= 3:
                rest = parts[2].lstrip("\n")
                if "## Description" not in rest and body:
                    rest = rest + "\n\n" + body if rest else body
                content = fm + "\n" + rest
        path.write_text(content, encoding="utf-8")
        return False

    path.write_text(content, encoding="utf-8")
    return True


def write_quadrant_files(by_quadrant: dict) -> None:
    for q in ["NW", "N", "NE", "E", "SE", "S", "SW", "W"]:
        label = QUADRANT_LABELS.get(q, q)
        path = VAULT / f"{label}.md"
        lines = [
            "---",
            f"title: {label}",
            f"description: Sword Coast locations in the {label} quadrant.",
            "---",
            "",
            f"# {label}",
            "",
        ]
        for note_name in sorted(by_quadrant.get(q, [])):
            lines.append(f"- [[{note_name}]]")
        lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not VAULT or str(VAULT) == str(SCRIPT_DIR):
        print("Error: Set vault_path in config.json (or create config from config.example.json).")
        return
    if not JSON_PATH.exists():
        print(f"Error: JSON file not found: {JSON_PATH}")
        return

    LOCATIONS_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    locations = [loc for loc in data.get("locations", []) if loc.get("name") and loc["name"] != "GROUP"]

    xs = [loc["x"] for loc in locations if "x" in loc]
    ys = [loc["y"] for loc in locations if "y" in loc]
    min_x = min(xs) if xs else 0
    max_x = max(xs) if xs else 1
    min_y = min(ys) if ys else 0
    max_y = max(ys) if ys else 1

    missing_wiki = []
    by_quadrant = {}
    created = 0
    updated = 0

    for loc in locations:
        name = loc["name"]
        x = loc.get("x", min_x)
        y = loc.get("y", min_y)
        map_quadrant = get_quadrant(x, y, min_x, max_x, min_y, max_y)
        region = get_region(x, y, min_x, max_x, min_y, max_y)

        wiki_link = guess_wiki_link(name) if UPDATE_WIKI_LINKS else ""
        if UPDATE_WIKI_LINKS and not wiki_link:
            missing_wiki.append(name)

        filename = safe_filename(name) + ".md"
        path = LOCATIONS_DIR / filename

        if write_note(path, loc, wiki_link, map_quadrant, region):
            created += 1
        else:
            updated += 1

        by_quadrant.setdefault(map_quadrant, []).append(name)

    if GENERATE_INDICES:
        write_quadrant_files(by_quadrant)

    if missing_wiki:
        WIKIFAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
        content = "---\ntitle: ~WikiFails~\ndescription: Locations where a wiki link could not be resolved.\n---\n\n# Missing wiki_link entries\n\n"
        for n in sorted(set(missing_wiki)):
            content += f"- {n}\n"
        WIKIFAILS_PATH.write_text(content, encoding="utf-8")

    print(f"Created {created} new notes, updated {updated} notes, {len(set(missing_wiki))} wiki links missing (see ~WikiFails~.md).")


if __name__ == "__main__":
    main()
