import pyzipper
import os
import sys
import json
from datetime import datetime

# --- Configuration ---
ZIP_PATH = "toffee.zip"
OUT_DIR = "."
CREATOR_NAME = "Asim_Dipto"

def update_playlist_logic():
    """এক্সট্রাক্ট করা api.json থেকে প্লেলিস্ট তৈরি করার লজিক"""
    source_json = "api.json"
    output_m3u = "Toffee_NS_Player.m3u"
    
    if os.path.exists(source_json):
        try:
            with open(source_json, "r", encoding="utf-8") as f:
                channels = json.load(f)
            
            # M3U ফরম্যাটে আপনার নাম (Credit) যোগ করা
            m3u_content = f"#EXTM3U\n#Creator: {CREATOR_NAME}\n#Update: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n\n"
            
            for ch in channels:
                name = ch.get("name", "Unknown")
                link = ch.get("link", "")
                logo = ch.get("logo", "")
                cat = ch.get("category_name", "Live TV")
                # api.json এ যদি কুকি থাকে তবে সেটি নেয়া হবে
                ck = ch.get("cookie", "") 
                
                m3u_content += f'#EXTINF:-1 group-title="{cat}" tvg-logo="{logo}", {name}\n'
                m3u_content += f'#EXTVLCOPT:http-user-agent=Toffee (Linux;Android 14)\n'
                if ck:
                    m3u_content += f'#EXTVLCOPT:http-cookie={ck}\n'
                m3u_content += f'{link}\n\n'
            
            # ফাইলটি সেভ করা
            with open(output_m3u, "w", encoding="utf-8") as f:
                f.write(m3u_content)
            
            # একই সাথে Ott Navigator এর জন্যও কপি তৈরি করা
            with open("Toffee_Ott_Navigator.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
                
            print(f"[+] Assets Generated with Creator: {CREATOR_NAME}")
            
        except Exception as e:
            print(f"[-] Logic Error: {e}")

# --- Main Execution ---
pwd = os.environ.get("ZIP_PWD")
if not pwd:
    print("Error: ZIP_PWD environment variable not set.")
    sys.exit(2)

if not os.path.exists(ZIP_PATH):
    print(f"Error: {ZIP_PATH} not found.")
    sys.exit(3)

try:
    # ১. জিপ ফাইল এক্সট্রাক্ট করা
    with pyzipper.AESZipFile(ZIP_PATH, 'r') as zf:
        zf.setpassword(pwd.encode())
        zf.extractall(path=OUT_DIR)
    print("[+] Extraction successful.")

    # ২. এক্সট্রাক্ট শেষ হলে অটোমেটিক প্লেলিস্ট এডিট করা
    update_playlist_logic()

except RuntimeError as e:
    print("Extraction failed (Possible wrong password):", e)
    sys.exit(4)
except Exception as e:
    print("Unexpected error:", e)
    sys.exit(5)
