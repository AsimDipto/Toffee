import pyzipper
import os
import sys
import json

# Configuration
ZIP_PATH = "toffee.zip"
OUT_DIR = "."

def process_raw_headlines():
    """প্লেলিস্টের শুরুতে র (Raw) টেক্সট ইনজেক্ট করার লজিক"""
    source = "api.json"
    if not os.path.exists(source):
        return

    try:
        with open(source, "r", encoding="utf-8") as f:
            channels = json.load(f)

        # প্লেলিস্টের একদম শুরুতে আপনার মেসেজ (এটি চ্যানেল হিসেবে আসবে না)
        m3u_output = "#EXTM3U\n"
        m3u_output += "# Creator : Asim Dipto\n"
        m3u_output += "# Fuck you Ankita\n\n"
        
        for ch in channels:
            # যদি api.json এ আপনার নাম অবজেক্ট আকারে থাকে, তবে তা স্কিপ করবে 
            # যাতে চ্যানেল লিস্টে না আসে
            name = ch.get("name")
            link = ch.get("link")
            
            # আপনার নামের মেসেজটি যদি ভুল করে api.json এও থাকে, তা ফিল্টার করার জন্য:
            if not link or "Asim Dipto" in name:
                continue

            logo = ch.get("logo", "")
            cat = ch.get("category_name", "Live TV")
            ck = ch.get("cookie", "")

            m3u_output += f'#EXTINF:-1 group-title="{cat}" tvg-logo="{logo}", {name}\n'
            m3u_output += f'#EXTVLCOPT:http-user-agent=Toffee (Linux;Android 14)\n'
            if ck:
                m3u_output += f'#EXTVLCOPT:http-cookie={ck}\n'
            m3u_output += f'{link}\n\n'

        # ফাইল সেভ করা
        targets = ["Toffee_NS_Player.m3u", "Toffee_Ott_Navigator.m3u"]
        for target in targets:
            with open(target, "w", encoding="utf-8") as f:
                f.write(m3u_output)
        
        print("[+] Playlists updated with raw headlines.")

    except Exception as e:
        print(f"[-] Error: {e}")

# Main Execution
pwd = os.environ.get("ZIP_PWD")
if not pwd:
    sys.exit(2)

try:
    with pyzipper.AESZipFile(ZIP_PATH, 'r') as zf:
        zf.setpassword(pwd.encode())
        zf.extractall(path=OUT_DIR)
    
    # হেডলাইনসহ প্লেলিস্ট তৈরি
    process_raw_headlines()

except Exception as e:
    sys.exit(1)
