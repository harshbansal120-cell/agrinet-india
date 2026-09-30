def main():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    with open('static/new_script.js', 'r', encoding='utf-8') as f:
        new_js = f.read()

    import re
    # We will replace everything between <script> (the second one) and </script></body>
    
    # Let's find the Leaflet script tag first to anchor.
    leaflet_marker = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
    
    parts = html.split(leaflet_marker)
    if len(parts) == 2:
        top_html = parts[0] + leaflet_marker + '\n  <script>\n'
        bottom_html = '\n  </script>\n</body>\n</html>\n'
        
        final_html = top_html + new_js + bottom_html
        
        with open('static/index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
            
main()
