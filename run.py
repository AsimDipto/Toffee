import pyzipper
import os
import sys
import json
from datetime import datetime

# --- Configuration ---
ZIP_PATH = "toffee.zip"
OUT_DIR = "."
CREDIT_NAME = "Asim_Dipto"

def build_custom_playlists():
    """Extract করা ডেটা থেকে ক্রেডিটসহ প্লেলিস্ট তৈরির মাস্টার ফাংশন"""
    data_source = "api.json"
    
    if not os.path.exists(data_source):
        print(f"[-] Error: {data_source} not found after extraction.")
        return

    try:
        with open(data_source, "r", encoding="utf-8") as f:
            channels = json.load(f)
        
        # আপনার নাম ও টাইমস্ট্যাম্পসহ M3U হেডার
        timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
        m3u_header = f"#EXTM3U\n#Creator: {CREDIT_NAME}\n#Update: {timestamp}\n\n"
        
        m3u_body = ""
        for ch in channels:
            name = ch.get("name", "Unknown")
            link = ch.get("link", "")
            logo = ch.get("logo", "")
            cat = ch.get("category_name", "Live TV")
            ck = ch.get("cookie", "")
            
            m3u_body += f'#EXTINF:-1 group-title="{cat}" tvg-logo="{logo}", {name}\n'
            m3u_body += f'#EXTVLCOPT:http-user-agent=Toffee (Linux;Android 14)\n'
            if ck:
                m3u_body += f'#EXTVLCOPT:http-cookie={ck}\n'
            m3u_body += f'{link}\n\n'
        
        full_content = m3u_header + m3u_body

        # ১. Toffee_NS_Player.m3u তৈরি
        with open("Toffee_NS_Player.m3u", "w", encoding="utf-8") as f:
            f.write(full_content)
            
        # ২. Toffee_Ott_Navigator.m3u তৈরি
        with open("Toffee_Ott_Navigator.m3u", "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"[+] Success: Playlists updated with Creator: {CREDIT_NAME}")

    except Exception as e:
        print(f"[-] Logic Error: {str(e)}")

# --- Core Execution ---
def main():
    pwd = os.environ.get("ZIP_PWD")
    if not pwd:
        print("[!] Error: ZIP_PWD is missing in environment.")
        sys.exit(2)

    if not os.path.exists(ZIP_PATH):
        print(f"[!] Error: {ZIP_PATH} file not found.")
        sys.exit(3)

    try:
        print("[*] Attempting to extract core assets...")
        with pyzipper.AESZipFile(ZIP_PATH, 'r') as zf:
            zf.setpassword(pwd.encode())
            zf.extractall(path=OUT_DIR)
        print("[+] Extraction completed.")

        # ফাইল আনজিপ হওয়ার পর আপনার ক্রেডিট যোগ করার কাজ শুরু হবে
        build_custom_playlists()

    except RuntimeError:
        print("[!] Error: Extraction failed (Wrong Password).")
        sys.exit(4)
    except Exception as e:
        print(f"[!] Unexpected System Error: {e}")
        sys.exit(5)

if __name__ == "__main__":
    main()
