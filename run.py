import pyzipper
import os
import sys
import json

# ফাইল পাথ কনফিগারেশন
ZIP_PATH = "toffee.zip"
OUT_DIR = "."

def write_playlists_with_header():
    """EXTM3U এর ঠিক নিচে হেডলাইন ইনজেক্ট করার লজিক"""
    source = "api.json"
    if not os.path.exists(source):
        print("Error: api.json file not found!")
        return

    try:
        with open(source, "r", encoding="utf-8") as f:
            channels = json.load(f)

        # আপনার র (Raw) হেডলাইন যা ফাইলের শুরুতে থাকবে
        # লাইনের শুরুতে # থাকলে প্লেয়ার এটাকে চ্যানেল মনে করবে না
        custom_header = "#EXTM3U\n"
        custom_header += "# Creator : Asim Dipto\n"
        custom_header += "# Fuck you Ankita\n\n"
        
        m3u_body = ""
        for ch in channels:
            name = ch.get("name")
            link = ch.get("link")
            logo = ch.get("logo", "")
            cat = ch.get("category_name", "Live TV")
            ck = ch.get("cookie", "")

            if name and link:
                m3u_body += f'#EXTINF:-1 group-title="{cat}" tvg-logo="{logo}", {name}\n'
                m3u_body += f'#EXTVLCOPT:http-user-agent=Toffee (Linux;Android 14)\n'
                if ck:
                    m3u_body += f'#EXTVLCOPT:http-cookie={ck}\n'
                m3u_body += f'{link}\n\n'

        # পুরো কন্টেন্ট একসাথে করা
        final_content = custom_header + m3u_body

        # ফাইলগুলো সেভ করা (Toffee_NS_Player এবং Toffee_Ott_Navigator)
        playlist_files = ["Toffee_NS_Player.m3u", "Toffee_Ott_Navigator.m3u"]
        for filename in playlist_files:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_content)
        
        print("[+] Header successfully injected into all playlists!")

    except Exception as e:
        print(f"[-] Execution Error: {e}")

# --- মেন প্রসেস ---
zip_pwd = os.environ.get("ZIP_PWD")
if not zip_pwd:
    print("ZIP_PWD environment variable missing!")
    sys.exit(2)

try:
    # ১. জিপ ফাইল আনজিপ করা
    if os.path.exists(ZIP_PATH):
        with pyzipper.AESZipFile(ZIP_PATH, 'r') as zf:
            zf.setpassword(zip_pwd.encode())
            zf.extractall(path=OUT_DIR)
        print("[+] Unzip successful.")
    
    # ২. আনজিপ হওয়ার পর আপনার হেডলাইনসহ প্লেলিস্ট তৈরি করা
    write_playlists_with_header()

except Exception as e:
    print(f"[-] Zip Process Error: {e}")
    sys.exit(1)
