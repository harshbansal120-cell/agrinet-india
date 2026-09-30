import re

def update_script():
    with open('static/new_script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # Replace place() function
    old_place = """function place(lat, lon) {
  if(pin) map.removeLayer(pin);
  pin = L.marker([lat, lon]).addTo(map);
    // Keep coordinates format raw
  $('pin-coords').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
}"""

    new_place = """function place(lat, lon) {
  if(pin) map.removeLayer(pin);
  pin = L.marker([lat, lon]).addTo(map);
  $('pin-coords').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
  if ($('lat-input')) $('lat-input').value = lat.toFixed(4);
  if ($('lon-input')) $('lon-input').value = lon.toFixed(4);
}"""

    js = js.replace(old_place, new_place)

    # Append coordinate input observers
    observers = """
function handleManualCoord() {
    let lat = parseFloat($('lat-input').value);
    let lon = parseFloat($('lon-input').value);
    if (!isNaN(lat) && !isNaN(lon)) {
        lon = normalizeLongitude(lon);
        if(pin) map.removeLayer(pin);
        pin = L.marker([lat, lon]).addTo(map);
        $('pin-coords').textContent = `${lat.toFixed(4)}, ${lon.toFixed(4)}`;
        map.setView([lat, lon]);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    if ($('lat-input')) $('lat-input').addEventListener('change', handleManualCoord);
    if ($('lon-input')) $('lon-input').addEventListener('change', handleManualCoord);
    // Bind Enter key as well
    if ($('lat-input')) $('lat-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') handleManualCoord(); });
    if ($('lon-input')) $('lon-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') handleManualCoord(); });
});
"""
    js = js + observers

    with open('static/new_script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print("Lat/Lon manual bindings injected.")

if __name__ == '__main__':
    update_script()
