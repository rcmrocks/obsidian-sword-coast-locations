# Obsidian Sword Coast Locations

Generate Obsidian notes for every location on the Sword Coast from the [AideDD interactive map](https://www.aidedd.org/atlas/sword-coast). One note per marker, with minimal frontmatter, quadrant indices, color tags, and optional wiki links.

**License:** [GNU General Public License v3.0](LICENSE). This project is not affiliated with AideDD or Obsidian.

---

## Prerequisites

- **Python 3.7+**
- A modern browser (to export the map data)
- An [Obsidian](https://obsidian.md) vault

## Quick start

1. **Clone this repo**
   ```bash
   git clone https://github.com/rcmrocks/obsidian-sword-coast-locations.git
   cd obsidian-sword-coast-locations
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get the location data**  
   Export `sword_coast_locations.json` from the AideDD map using the browser snippet. See [Exporting the map data](docs/export-map.md).

4. **Configure paths**  
   Copy `config.example.json` to `config.json` and set:
   - `vault_path` – path to your Obsidian vault folder
   - `json_path` – path to `sword_coast_locations.json`

5. **Run the generator**
   ```bash
   python generate_obsidian_locations.py
   ```

At the end you’ll see a summary like:  
`Created X new notes, updated Y notes, Z wiki links missing (see ~WikiFails~.md).`

---

## What you get

- **Locations folder** in your vault: one `.md` file per location with:
  - **Frontmatter:** `name`, `type`, `region`, `map_quadrant`, `map_link`, `wiki_link`, `tags` (including a color tag from the map)
  - **Body:** optional `## Description` section with AideDD description text
- **Eight index files** in the vault root: **North West.md**, **North.md**, **North East.md**, **East.md**, **South East.md**, **South.md**, **South West.md**, **West.md** – each lists `[[Location Name]]` for that quadrant
- **~WikiFails~.md** – locations where no Forgotten Realms wiki link was found (you can add links manually)

## Color tags

Each location gets a tag from the AideDD marker color:

| Tag            | Hex     | Meaning     |
|----------------|---------|-------------|
| `color-ffffff` | #ffffff | Area        |
| `color-33cc33` | #33cc33 | Forest      |
| `color-ff8000` | #ff8000 | Mountainous |
| `color-ff0000` | #ff0000 | Place       |
| `color-58acfa` | #58acfa | Water       |
| `color-f781f3` | #f781f3 | Road        |

## Configuration

In `config.json` (or the CONFIGURATION block at the top of the script if no config file exists):

| Option               | Default | Description |
|----------------------|---------|-------------|
| `vault_path`         | (required) | Path to your Obsidian vault |
| `json_path`          | (required) | Path to `sword_coast_locations.json` |
| `overwrite_existing` | `false` | If `true`, overwrite existing location notes |
| `include_descriptions` | `true` | Add `## Description` from AideDD when present |
| `generate_indices`   | `true` | Rebuild the eight quadrant index files |
| `update_wiki_links`  | `true` | Try to resolve Forgotten Realms wiki URLs |

## Troubleshooting

- **"JSON file not found"** – Check `json_path` in `config.json` and that you ran the browser snippet and saved the downloaded file.
- **No notes created** – Ensure `vault_path` points to the vault folder (the one containing `.obsidian`).
- **Wiki lookup slow or failing** – Set `update_wiki_links` to `false` to skip Fandom lookups; you can add links later in frontmatter.

## Other AideDD maps

The script is built for the Sword Coast / Faerûn map. Other AideDD maps (e.g. Waterdeep, Icewind Dale) may work if you export JSON in the same shape (`name`, `type`, `description`, `x`, `y`, `color`). Adapt paths and run as needed.
