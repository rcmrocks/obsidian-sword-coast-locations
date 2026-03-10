# Exporting the map data from AideDD

The generator needs a JSON file with every location on the Sword Coast map. You get that by running a small script in your browser on the AideDD page.

## Steps

1. Open the **Sword Coast** interactive map:  
   [https://www.aidedd.org/atlas/sword-coast](https://www.aidedd.org/atlas/sword-coast)

2. Wait until the map is fully loaded (you can zoom or pan to be sure).

3. Open your browser’s **Developer Tools**:
   - Windows/Linux: `F12` or `Ctrl+Shift+I`
   - Mac: `Cmd+Option+I`

4. Go to the **Console** tab.

5. Open the file `browser-snippet.js` from this repo, copy its entire contents, paste into the console, and press **Enter**.

6. A file named **sword_coast_locations.json** should download. Move it somewhere handy (e.g. next to the generator script or into a `data` folder).

7. In **config.json**, set `json_path` to the full path of that file (e.g. `C:\Users\You\obsidian-sword-coast-locations\sword_coast_locations.json`).

## Expected JSON shape

The file should look like:

```json
{
  "source": "AideDD Sword Coast",
  "locations": [
    {
      "name": "Waterdeep",
      "type": "Place",
      "description": "<p>...</p>",
      "x": 1234,
      "y": 5678,
      "color": "#ff0000"
    }
  ]
}
```

If your export has the same fields, the generator will work. If AideDD change their page and the snippet stops working, open an issue on the repo.
