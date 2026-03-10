/**
 * AideDD Sword Coast – export all markers to JSON
 *
 * 1. Open https://www.aidedd.org/atlas/sword-coast
 * 2. Wait for the map to load fully
 * 3. Open DevTools (F12) → Console
 * 4. Paste this entire file and press Enter
 * 5. Save the downloaded sword_coast_locations.json and use its path in config.json
 */
(function () {
  var colorToType = {
    "#ffffff": "Area",
    "#33cc33": "Forest",
    "#ff8000": "Mountainous",
    "#ff0000": "Place",
    "#58acfa": "Water",
    "#f781f3": "Road",
  };

  var raw = (window.groupe || []);
  if (!Array.isArray(raw) || raw.length === 0) {
    console.error("No 'groupe' array found. Make sure the map is fully loaded, then try again.");
    return;
  }

  var locations = raw
    .map(function (item) {
      var name = item.name || item.name1 || item.name2 || "";
      var color = (item.color || "").toLowerCase();
      var type = colorToType[color] || "Unknown";
      var description = item.txt || item.txt1 || item.txt0 || "";
      var x = item.x;
      var y = item.y;
      return { name: name, type: type, description: description, x: x, y: y, color: color };
    })
    .filter(function (loc) {
      return loc.name && loc.name !== "GROUP";
    });

  console.log("Exporting " + locations.length + " locations…");

  var data = { source: "AideDD Sword Coast", locations: locations };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = "sword_coast_locations.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
})();
