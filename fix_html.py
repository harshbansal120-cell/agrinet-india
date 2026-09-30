import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the leaflet script
leaflet_idx = html.find('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')

if leaflet_idx != -1:
    # Find the next <script> tag
    script_start = html.find('<script>', leaflet_idx)
    # Find the closing </script> tag for the inline script
    # It should be the last </script> in the file.
    script_end = html.rfind('</script>')
    
    if script_start != -1 and script_end != -1 and script_end > script_start:
        new_html = html[:script_start] + '<script src="/static/new_script.js"></script>\n' + html[script_end+9:]
        with open('static/index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Successfully replaced inline script with new_script.js")
    else:
        print("Failed to find script bounds after leaflet")
else:
    print("Failed to find leaflet script tag")
