import re

def update_html():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    new_html = """            <div class="network-viz" style="margin-top: 24px; padding: 32px; flex-direction: column; justify-content: flex-start; align-items: stretch; height: auto; min-height: 300px; background: url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22><circle cx=%222%22 cy=%222%22 r=%221%22 fill=%22%23e5e7eb%22/></svg>');">
               
               <div style="background:rgba(255,255,255,0.95); padding: 20px; border-radius: 8px; border:1px solid var(--border); margin-bottom: 24px; text-align: center; font-weight: 500; font-size: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
                   <span style="color:var(--text-main)">State Data</span> <span style="color:#d1d5db">➔</span> 
                   <span style="color:var(--primary)">AgriNet Common Schema</span> <span style="color:#d1d5db">➔</span> 
                   <span style="color:var(--text-main)">AI Intelligence</span> <span style="color:#d1d5db">➔</span> 
                   <span style="color:#b45309">Localized Advisory</span>
               </div>
               
               <div style="background:rgba(255,255,255,0.95); padding: 12px; border-radius: 8px; border:1px solid var(--border); overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
                   <table style="width:100%; border-collapse: collapse; font-size:13px; text-align: left;">
                     <thead>
                       <tr style="border-bottom: 1px solid var(--border); color: #666;">
                         <th style="padding: 10px;">State</th>
                         <th style="padding: 10px;">Demo / Pilot Field</th>
                         <th style="padding: 10px;">Crop</th>
                         <th style="padding: 10px;">Intelligence</th>
                       </tr>
                     </thead>
                     <tbody>
                       <tr style="border-bottom: 1px solid #f3f4f6;">
                         <td style="padding: 10px; font-weight: 500; display: flex; align-items: center; gap: 6px;"><div style="width:6px; height:6px; border-radius:50%; background:#10b981;"></div> Uttar Pradesh</td>
                         <td style="padding: 10px; color: #444;">Agra</td>
                         <td style="padding: 10px;"><span class="badge badge-demo" style="background:#f0ebd8; color:#786620; border:1px solid #dcd4b8">Wheat</span></td>
                         <td style="padding: 10px; color: #666;">Satellite + Soil + Weather + Gemini</td>
                       </tr>
                       <tr style="border-bottom: 1px solid #f3f4f6;">
                         <td style="padding: 10px; font-weight: 500; display: flex; align-items: center; gap: 6px;"><div style="width:6px; height:6px; border-radius:50%; background:#10b981;"></div> Punjab</td>
                         <td style="padding: 10px; color: #444;">Ludhiana</td>
                         <td style="padding: 10px;"><span class="badge badge-demo" style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd">Rice</span></td>
                         <td style="padding: 10px; color: #666;">Satellite + Soil + Weather + Gemini</td>
                       </tr>
                       <tr style="border-bottom: 1px solid #f3f4f6;">
                         <td style="padding: 10px; font-weight: 500; display: flex; align-items: center; gap: 6px;"><div style="width:6px; height:6px; border-radius:50%; background:#10b981;"></div> Maharashtra</td>
                         <td style="padding: 10px; color: #444;">Nashik</td>
                         <td style="padding: 10px;"><span class="badge badge-demo">Cotton</span></td>
                         <td style="padding: 10px; color: #666;">Satellite + Soil + Weather + Gemini</td>
                       </tr>
                       <tr style="border-bottom: 1px solid #f3f4f6;">
                         <td style="padding: 10px; font-weight: 500; display: flex; align-items: center; gap: 6px;"><div style="width:6px; height:6px; border-radius:50%; background:#10b981;"></div> Andhra Pradesh</td>
                         <td style="padding: 10px; color: #444;">Guntur</td>
                         <td style="padding: 10px;"><span class="badge badge-demo" style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd">Rice</span></td>
                         <td style="padding: 10px; color: #666;">Satellite + Soil + Weather + Gemini</td>
                       </tr>
                       <tr style="border-bottom: 1px solid #f3f4f6;">
                         <td style="padding: 10px; font-weight: 500; display: flex; align-items: center; gap: 6px;"><div style="width:6px; height:6px; border-radius:50%; background:#10b981;"></div> Tamil Nadu</td>
                         <td style="padding: 10px; color: #444;">Villupuram</td>
                         <td style="padding: 10px;"><span class="badge badge-demo" style="background:#fef3c7; color:#b45309; border:1px solid #fde68a">Groundnut</span></td>
                         <td style="padding: 10px; color: #666;">Satellite + Soil + Weather + Gemini</td>
                       </tr>
                       <tr>
                         <td style="padding: 10px; font-weight: 500; display: flex; align-items: center; gap: 6px;"><div style="width:6px; height:6px; border-radius:50%; background:#10b981;"></div> Odisha</td>
                         <td style="padding: 10px; color: #444;">Sambalpur</td>
                         <td style="padding: 10px;"><span class="badge badge-demo" style="background:#ffedd5; color:#c2410c; border:1px solid #fed7aa">Sorghum</span></td>
                         <td style="padding: 10px; color: #666;">Satellite + Soil + Weather + Gemini</td>
                       </tr>
                     </tbody>
                   </table>
               </div>
            </div>"""

    start_idx = html.find('<div class="network-viz"')
    end_idx = html.find('</div>\n          </div>', start_idx)
    
    if start_idx != -1 and end_idx != -1:
        # We want to replace everything from start_idx up to end_idx 
        # But wait, there are nested divs.
        
        # Let's use regex or string replace.
        content_to_replace = html[start_idx:end_idx]
        html = html.replace(content_to_replace, new_html)
        
        with open('static/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated HTML visualization.")
    else:
        print("Failed to find network-viz boundaries.")

def update_lang():
    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    # Change all occurrences of AgriNet Interoperability Pilot -> 🇮🇳 India Agricultural Intelligence Network
    js = js.replace('"AgriNet Interoperability Pilot"', '"🇮🇳 India Agricultural Intelligence Network"')
    # Same for subtitle
    js = js.replace('"One intelligence schema. Configurable state adapters."', '"One interoperable intelligence layer. State-specific data adapters."')

    # Also handle hindi and other translations if they were explicitly defined manually earlier
    js = js.replace('"अंतरसंचालनीयता पायलट"', '"🇮🇳 India Agricultural Intelligence Network"')
    js = js.replace('"इంటర్‌ఆపెరబిలిటీ పైలట్"', '"🇮🇳 India Agricultural Intelligence Network"')
    js = js.replace('"ইন্টারঅপারেবিলিটি পাইলট পরিস্থিতি"', '"🇮🇳 India Agricultural Intelligence Network"')
    js = js.replace('"রাష్ట్ర నెట్‌వర్క్ మూల్యాంకనం కోసం ప్రదర్శన క్షేత్రాలు."', '"One interoperable intelligence layer. State-specific data adapters."')
    js = js.replace('"নেটওয়ার্ক মূল্যায়নের জন্য প্রাক-কনফিগার করা ক্ষেত্র।"', '"One interoperable intelligence layer. State-specific data adapters."')

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated language configs.")

if __name__ == '__main__':
    update_html()
    update_lang()
