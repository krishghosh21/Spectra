#!/usr/bin/env python3
"""
Instagram Profile Tool  -  enhanced UI edition
(instagrapi / mobile API)

Use only with a session that belongs to you or that you are authorized to use.
Needs a truecolor terminal (Windows Terminal, iTerm2, GNOME Terminal, VS Code, etc).
"""

import os
import re
import sys
import json
import time
import shutil
import textwrap
import itertools
import threading
import webbrowser

from pathlib import Path
from datetime import datetime

import requests
from instagrapi import Client


# ============================================================
# CONFIG
# ============================================================

EXPORT_ROOT = Path("instagram_export")

FOLLOWER_PAGE_SIZE = 200
FOLLOWING_PAGE_SIZE = 200
POST_PAGE_SIZE = 12

# 0 = fetch all available
FOLLOWER_LIMIT = 0
FOLLOWING_LIMIT = 0
POST_LIMIT = 0

BOX_WIDTH = 68
ANIMATE = True          # set False to disable banner animation

MEDIA_TYPES = {1: "Photo", 2: "Video", 8: "Album"}


# ============================================================
# COLORS  (truecolor palette)
# ============================================================

if os.name == "nt":
    os.system("")  # enables ANSI escape processing on Windows 10+


def fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

PINK = fg(255, 95, 162)
PURPLE = fg(168, 85, 247)
ORANGE = fg(255, 149, 0)
YELLOW = fg(255, 214, 10)
CYAN = fg(34, 211, 238)
BLUE = fg(96, 165, 250)
GREEN = fg(74, 222, 128)
RED = fg(248, 113, 113)
WHITE = fg(240, 240, 245)
GRAY = fg(130, 135, 150)

# Instagram-style gradient: purple -> red -> orange -> yellow
IG_STOPS = [
    (131, 58, 180),
    (225, 48, 108),
    (253, 29, 29),
    (252, 176, 69),
]

ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def vlen(s):
    """Visible length of a string (ANSI codes stripped)."""
    return len(ANSI_RE.sub("", s))


def pad(s, width):
    return s + " " * max(0, width - vlen(s))


def clip(s, n):
    s = str(s)
    return s if len(s) <= n else s[: max(0, n - 1)] + "…"


def color_at(t, stops=IG_STOPS):
    t = max(0.0, min(1.0, t))
    scaled = t * (len(stops) - 1)
    i = min(int(scaled), len(stops) - 2)
    f = scaled - i
    a, b = stops[i], stops[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))


def gradient_text(text, stops=IG_STOPS, shift=0.0, span=1.0):
    n = max(len(text) - 1, 1)
    out = []
    for i, ch in enumerate(text):
        if ch == " ":
            out.append(ch)
            continue
        r, g, b = color_at(i / n * span + shift, stops)
        out.append(fg(r, g, b) + ch)
    return "".join(out) + RESET


# ============================================================
# TERMINAL HELPERS
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(f"\n{GRAY}Press {WHITE}ENTER{GRAY} to continue...{RESET}")


def ok(text):
    print(f"{GREEN}[✓]{RESET} {text}")


def info(text):
    print(f"{CYAN}[*]{RESET} {text}")


def warn(text):
    print(f"{YELLOW}[!]{RESET} {YELLOW}{text}{RESET}")


def err(text):
    print(f"{RED}[✗]{RESET} {RED}{text}{RESET}")


def dim(text):
    print(f"{GRAY}{text}{RESET}")


def ask(prompt):
    return input(f"{PINK}❯{RESET} {WHITE}{prompt}{RESET}{GRAY}: {RESET}").strip()


def safe_filename(name):
    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789_-"
    )
    return "".join(c if c in allowed else "_" for c in name)


class Spinner:
    """Context-manager braille spinner."""

    FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(self, text):
        self.text = text
        self._stop = threading.Event()
        self._thread = None

    def _run(self):
        for i, frame in zip(itertools.count(), itertools.cycle(self.FRAMES)):
            if self._stop.is_set():
                break
            r, g, b = color_at((i % 20) / 20)
            print(
                f"\r\033[K{fg(r, g, b)}{frame}{RESET} {CYAN}{self.text}{RESET}",
                end="",
                flush=True,
            )
            time.sleep(0.08)

    def __enter__(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._thread.join()
        print("\r\033[K", end="", flush=True)


def progress(label, current, total=None, width=26):
    if total:
        ratio = min(current / total, 1.0)
        filled = int(width * ratio)
        bar = gradient_text("█" * filled) + GRAY + "░" * (width - filled) + RESET
        print(
            f"\r\033[K{CYAN}{label:<10}{RESET} {bar} "
            f"{WHITE}{current}{GRAY}/{total}  {ratio * 100:5.1f}%{RESET}",
            end="",
            flush=True,
        )
    else:
        print(
            f"\r\033[K{CYAN}{label:<10}{RESET} "
            f"{GREEN}{current}{RESET} {GRAY}fetched{RESET}",
            end="",
            flush=True,
        )


# ============================================================
# BOXES / LAYOUT
# ============================================================

def draw_box(title, rows, color=PINK, width=BOX_WIDTH):
    """rows: list of strings (may contain ANSI). None = separator."""
    inner = width - 2
    t = f" {title} " if title else ""
    left = (inner - len(t)) // 2
    right = inner - len(t) - left

    print(
        f"{color}╭{'─' * left}{RESET}{BOLD}{WHITE}{t}{RESET}"
        f"{color}{'─' * right}╮{RESET}"
    )

    for row in rows:
        if row is None:
            print(f"{color}├{'─' * inner}┤{RESET}")
        else:
            print(f"{color}│{RESET} {pad(row, inner - 2)} {color}│{RESET}")

    print(f"{color}╰{'─' * inner}╯{RESET}")


def kv(label, value, color=WHITE, width=BOX_WIDTH):
    room = width - 4 - 16
    return f"{GRAY}{label:<15}{RESET} {color}{clip(value, room)}{RESET}"


def section(title):
    print()
    print(gradient_text(f"══════ {title} ══════"))


# ============================================================
# BANNER
# ============================================================

BANNER_LINES = [
    "██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗",
    "██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║",
    "██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗██████╔╝███████║██╔████╔██║",
    "██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║",
    "██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║",
    "╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝",
]


def banner():
    term = shutil.get_terminal_size((100, 30)).columns
    art_w = len(BANNER_LINES[0])

    print()

    if term < art_w + 2:
        # narrow terminal fallback
        print(gradient_text("  ◆ INSTAGRAM PROFILE TOOL ◆", span=1.0))
    else:
        for row, line in enumerate(BANNER_LINES):
            print(" " + gradient_text(line, shift=row * 0.03, span=0.85))
            if ANIMATE:
                time.sleep(0.05)

    tagline = "P R O F I L E   T O O L   ·   mobile API edition"
    print()
    print(" " + gradient_text("━" * min(art_w, max(term - 2, 20))))
    print(f" {GRAY}{tagline.center(min(art_w, max(term - 2, 20)))}{RESET}")
    print(" " + gradient_text("━" * min(art_w, max(term - 2, 20))))
    print()


# ============================================================
# SERIALIZER
# ============================================================

def serialize(obj):

    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [serialize(v) for v in obj]

    if hasattr(obj, "model_dump"):
        try:
            return serialize(obj.model_dump())
        except Exception:
            pass

    if hasattr(obj, "dict"):
        try:
            return serialize(obj.dict())
        except Exception:
            pass

    if hasattr(obj, "__dict__"):
        return {
            key: serialize(value)
            for key, value in vars(obj).items()
            if not key.startswith("_")
        }

    return str(obj)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(serialize(data), f, indent=4, ensure_ascii=False)


# ============================================================
# SESSION
# ============================================================

def authenticate():

    draw_box(
        "NOTICE",
        [
            f"{YELLOW}Use only an Instagram session belonging to you{RESET}",
            f"{YELLOW}or an account you are authorized to use.{RESET}",
        ],
        color=YELLOW,
    )
    print()

    sessionid = ask("Enter sessionid")

    if not sessionid:
        err("Session ID cannot be empty.")
        sys.exit(1)

    print()

    try:
        with Spinner("Authenticating session"):
            cl = Client()
            result = cl.login_by_sessionid(sessionid)

        if not result:
            raise RuntimeError("Session authentication returned False")

        ok("Session accepted")

    except Exception as e:
        err("Authentication failed")
        dim(str(e))
        sys.exit(1)

    # Validate mobile/private access
    try:
        with Spinner("Checking mobile API access"):
            me = cl.account_info()

        ok(f"Logged in as {BOLD}{GREEN}@{me.username}{RESET}")

    except Exception as e:
        err("Mobile API validation failed")
        dim(str(e))
        print()
        warn(
            "The supplied session may be accepted for some public lookups "
            "but rejected by private/mobile endpoints."
        )
        sys.exit(1)

    return cl


# ============================================================
# PROFILE
# ============================================================

def get_profile(cl, username):

    try:
        with Spinner(f"Looking up @{username}"):
            user = cl.user_info_by_username(username)

        ok("Profile found")
        return user

    except Exception as e:
        err(f"Profile lookup failed: {e}")
        return None


def show_profile(user):

    g = lambda name, default=None: getattr(user, name, default)

    username = g("username", "N/A")
    full_name = g("full_name", "") or "—"
    bio = g("biography", "") or "No biography"
    pic = g("profile_pic_url")
    ext = g("external_url")

    badges = []
    badges.append(f"{GREEN}✔ VERIFIED{RESET}" if g("is_verified") else f"{GRAY}○ not verified{RESET}")
    badges.append(f"{RED}● PRIVATE{RESET}" if g("is_private") else f"{GREEN}● PUBLIC{RESET}")
    if g("is_business"):
        badges.append(f"{BLUE}◆ BUSINESS{RESET}")

    stats = "   ".join(
        f"{BOLD}{YELLOW}{v:,}{RESET} {GRAY}{l}{RESET}"
        for l, v in (
            ("posts", g("media_count", 0) or 0),
            ("followers", g("follower_count", 0) or 0),
            ("following", g("following_count", 0) or 0),
        )
    )

    rows = [
        kv("Username", f"@{username}", GREEN),
        kv("Name", full_name, WHITE),
        kv("User ID", g("pk", "N/A"), GRAY),
        None,
        stats,
        None,
        "  ".join(badges),
    ]

    if ext:
        rows.append(kv("Link", ext, CYAN))

    rows.append(None)
    rows.append(f"{GRAY}Biography{RESET}")

    for line in bio.splitlines() or [bio]:
        for wrapped in textwrap.wrap(line, BOX_WIDTH - 8) or [""]:
            rows.append(f"  {WHITE}{wrapped}{RESET}")

    rows.append(None)
    rows.append(
        kv(
            "Profile picture",
            "Available" if pic else "Unavailable",
            GREEN if pic else RED,
        )
    )

    print()
    draw_box("PROFILE INFORMATION", rows, color=PINK)


# ============================================================
# ITERATION HELPER (works even if iter_* helpers are missing)
# ============================================================

def iterate(cl, iter_name, fallback_name, *args, amount, page_size):
    it = getattr(cl, iter_name, None)
    if it:
        yield from it(*args, amount=amount, page_size=page_size)
    else:
        yield from getattr(cl, fallback_name)(*args, amount=amount)


def collect(label, iterator, reported=None):
    """Consume iterator into a dict keyed by pk with live progress."""
    items = {}
    try:
        for obj in iterator:
            items[str(obj.pk)] = obj
            progress(label, len(items), reported or None)
        print()
        ok(f"Retrieved {BOLD}{len(items)}{RESET} {label.lower()}")
    except Exception as e:
        print()
        err(f"{label} failed: {e}")
    return items


def compare_counts(fetched, reported):
    if reported is None:
        return
    dim(f"    Profile reports: {reported}")
    if fetched != reported:
        warn("    Retrieved list does not match profile count.")


# ============================================================
# POSTS
# ============================================================

def fetch_posts(cl, user_id, reported=None):
    print()
    info("Fetching posts using mobile API...")
    data = collect(
        "Posts",
        iterate(
            cl, "iter_user_medias", "user_medias", user_id,
            amount=POST_LIMIT, page_size=POST_PAGE_SIZE,
        ),
        reported,
    )
    return list(data.values())


def post_link(media):
    code = getattr(media, "code", None)
    return f"https://www.instagram.com/p/{code}/" if code else None


def show_posts(posts):

    section("POSTS")

    if not posts:
        warn("No posts found.")
        return

    print()

    for index, media in enumerate(posts, start=1):

        caption = (getattr(media, "caption_text", "") or "").replace("\n", " ")
        likes = getattr(media, "like_count", 0)
        comments = getattr(media, "comment_count", 0)
        kind = MEDIA_TYPES.get(getattr(media, "media_type", None), "?")
        taken = getattr(media, "taken_at", None)
        date = taken.strftime("%Y-%m-%d") if hasattr(taken, "strftime") else "—"
        link = post_link(media)

        r, g, b = color_at(min(index / max(len(posts), 1), 1))
        c = fg(r, g, b)

        print(
            f"{c}┌─{RESET} {BOLD}{WHITE}#{index:03d}{RESET} "
            f"{GRAY}{media.pk}{RESET}  {PURPLE}[{kind}]{RESET}"
        )
        print(
            f"{c}│{RESET}  {GRAY}♥{RESET} {YELLOW}{likes}{RESET}   "
            f"{GRAY}✎{RESET} {YELLOW}{comments}{RESET}   "
            f"{GRAY}{date}{RESET}"
        )
        if link:
            print(f"{c}│{RESET}  {CYAN}{link}{RESET}")
        if caption:
            print(f"{c}│{RESET}  {GRAY}{clip(caption, 110)}{RESET}")
        print(f"{c}└{'─' * 40}{RESET}")


# ============================================================
# FOLLOWERS / FOLLOWING
# ============================================================

def fetch_followers(cl, user_id, reported_count):
    print()
    info("Fetching followers using mobile API...")
    data = collect(
        "Followers",
        iterate(
            cl, "iter_user_followers_v1", "user_followers_v1", str(user_id),
            amount=FOLLOWER_LIMIT, page_size=FOLLOWER_PAGE_SIZE,
        ),
        reported_count,
    )
    compare_counts(len(data), reported_count)
    return data


def fetch_following(cl, user_id, reported_count):
    print()
    info("Fetching following using mobile API...")
    data = collect(
        "Following",
        iterate(
            cl, "iter_user_following_v1", "user_following_v1", str(user_id),
            amount=FOLLOWING_LIMIT, page_size=FOLLOWING_PAGE_SIZE,
        ),
        reported_count,
    )
    compare_counts(len(data), reported_count)
    return data


def show_user_list(users, title, reported_count=None):

    section(title)

    extra = f"  {GRAY}|  profile count: {WHITE}{reported_count}{RESET}" if reported_count is not None else ""
    print(f"{GRAY}fetched: {WHITE}{len(users)}{RESET}{extra}")
    print()

    if not users:
        warn("No users available.")
        return

    print(
        f"{GRAY}{'#':>5}  {'USERNAME':<30} {'NAME':<28} FLAGS{RESET}"
    )
    print(gradient_text("─" * 76))

    for index, person in enumerate(users.values(), start=1):

        username = getattr(person, "username", "unknown")
        full_name = getattr(person, "full_name", "") or ""

        flags = ""
        if getattr(person, "is_verified", False):
            flags += f"{GREEN}✔{RESET} "
        if getattr(person, "is_private", False):
            flags += f"{RED}●{RESET}"

        r, g, b = color_at(index / max(len(users), 1))

        print(
            f"{fg(r, g, b)}{index:>5}{RESET}  "
            f"{GREEN}{clip('@' + username, 30):<30}{RESET} "
            f"{GRAY}{clip(full_name, 28):<28}{RESET} {flags}"
        )

    print()
    dim("  ✔ verified   ● private")


# ============================================================
# PROFILE PICTURE
# ============================================================

def download_profile_picture(user, directory):

    url = getattr(user, "profile_pic_url", None)

    if not url:
        warn("Profile picture URL unavailable.")
        return None

    info("Downloading profile picture directly...")

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0 Safari/537.36"
            )
        }

        with Spinner("Downloading"):
            response = requests.get(
                str(url), headers=headers, timeout=30, allow_redirects=True
            )
            response.raise_for_status()

        output = Path(directory) / "profile_picture.jpg"
        output.write_bytes(response.content)

        ok(f"Profile picture saved: {CYAN}{output}{RESET}")
        return output

    except Exception as e:
        warn(f"Profile picture download failed: {e}")
        return None


# ============================================================
# DOWNLOAD POST MEDIA
# ============================================================

def download_post_media(cl, posts, directory):

    if not posts:
        return

    print()
    info("Downloading post media...")

    success = 0
    failed = 0
    total = len(posts)

    for index, media in enumerate(posts, start=1):

        try:
            media_type = getattr(media, "media_type", None)

            if media_type == 1:
                cl.photo_download(media.pk, folder=Path(directory))
            elif media_type == 2:
                cl.video_download(media.pk, folder=Path(directory))
            elif media_type == 8:
                cl.album_download(media.pk, folder=Path(directory))
            else:
                print()
                warn(f"Post {index}: unsupported media type {media_type}")
                continue

            success += 1

        except Exception as e:
            failed += 1
            print()
            warn(f"Post {index} failed: {e}")

        progress("Media", index, total)

    print()
    ok(f"Downloaded: {success}")
    if failed:
        warn(f"Failed: {failed}")


# ============================================================
# FULL EXPORT
# ============================================================

def full_export(cl, user, posts, followers, following):

    username = safe_filename(user.username)
    export_dir = EXPORT_ROOT / username
    posts_dir = export_dir / "posts"

    export_dir.mkdir(parents=True, exist_ok=True)
    posts_dir.mkdir(parents=True, exist_ok=True)

    print()
    info(f"Export directory: {CYAN}{export_dir}{RESET}")
    print()

    reported_followers = getattr(user, "follower_count", None)
    reported_following = getattr(user, "following_count", None)
    reported_posts = getattr(user, "media_count", None)

    # PROFILE
    save_json(export_dir / "profile.json", user)
    ok("profile.json saved")

    # PROFILE PICTURE URL
    (export_dir / "profile_picture_url.txt").write_text(
        str(getattr(user, "profile_pic_url", None) or ""), encoding="utf-8"
    )
    ok("profile_picture_url.txt saved")

    # FOLLOWERS / FOLLOWING / POSTS
    save_json(export_dir / "followers.json", followers)
    ok(f"followers.json saved ({len(followers)} fetched)")

    save_json(export_dir / "following.json", following)
    ok(f"following.json saved ({len(following)} fetched)")

    save_json(export_dir / "posts.json", posts)
    ok(f"posts.json saved ({len(posts)} fetched)")

    # MEDIA
    download_profile_picture(user, export_dir)
    download_post_media(cl, posts, posts_dir)

    # SUMMARY
    summary = {
        "export_time": datetime.now().isoformat(),
        "username": user.username,
        "user_id": str(user.pk),
        "reported_by_profile": {
            "followers": reported_followers,
            "following": reported_following,
            "posts": reported_posts,
        },
        "actually_fetched": {
            "followers": len(followers),
            "following": len(following),
            "posts": len(posts),
        },
        "complete_match": {
            "followers": (
                len(followers) == reported_followers
                if reported_followers is not None else False
            ),
            "following": (
                len(following) == reported_following
                if reported_following is not None else False
            ),
            "posts": (
                len(posts) == reported_posts
                if reported_posts is not None else False
            ),
        },
        "directory": str(export_dir),
    }

    save_json(export_dir / "data_summary.json", summary)

    def cell(fetched, reported):
        match = reported is not None and fetched == reported
        mark = f"{GREEN}✔{RESET}" if match else f"{YELLOW}≠{RESET}"
        return f"{WHITE}{fetched}{RESET}{GRAY} / {reported}{RESET} {mark}"

    print()
    draw_box(
        "EXPORT COMPLETED",
        [
            f"{GRAY}{'':<12}{'fetched / reported':>20}{RESET}",
            None,
            f"{CYAN}{'Followers':<12}{RESET}{cell(len(followers), reported_followers)}",
            f"{CYAN}{'Following':<12}{RESET}{cell(len(following), reported_following)}",
            f"{CYAN}{'Posts':<12}{RESET}{cell(len(posts), reported_posts)}",
            None,
            f"{GRAY}Saved to{RESET} {GREEN}{clip(str(export_dir), BOX_WIDTH - 16)}{RESET}",
        ],
        color=GREEN,
    )


# ============================================================
# OPEN PROFILE
# ============================================================

def open_profile(username):

    url = f"https://www.instagram.com/{username}/"
    print(f"{GREEN}{url}{RESET}")

    try:
        webbrowser.open(url)
    except Exception:
        pass


# ============================================================
# MENU
# ============================================================

MENU_ITEMS = [
    ("1", "Profile information"),
    ("2", "Profile picture URL"),
    ("3", "All posts + links"),
    ("4", "All followers"),
    ("5", "All following"),
    ("6", "Open Instagram profile"),
    ("7", "Download ALL details"),
    ("8", "Full terminal report"),
]


def show_menu(user):
    rows = []
    for key, label in MENU_ITEMS:
        rows.append(f"{gradient_text('[' + key + ']')}  {WHITE}{label}{RESET}")
    rows.append(None)
    rows.append(f"{RED}[0]{RESET}  {GRAY}Exit{RESET}")

    print()
    draw_box(f"MAIN MENU · @{user.username}", rows, color=PURPLE)


# ============================================================
# MAIN
# ============================================================

def main():

    clear()
    banner()

    cl = authenticate()

    print()

    target = ask("Enter Instagram username").lstrip("@")

    if not target:
        err("Username cannot be empty.")
        return

    user = get_profile(cl, target)

    if not user:
        return

    user_id = user.pk
    reported_followers = getattr(user, "follower_count", None)
    reported_following = getattr(user, "following_count", None)
    reported_posts = getattr(user, "media_count", None)

    # Cache
    cache = {"posts": None, "followers": None, "following": None}

    def get_posts():
        if cache["posts"] is None:
            cache["posts"] = fetch_posts(cl, user_id, reported_posts)
        return cache["posts"]

    def get_followers():
        if cache["followers"] is None:
            cache["followers"] = fetch_followers(cl, user_id, reported_followers)
        return cache["followers"]

    def get_following():
        if cache["following"] is None:
            cache["following"] = fetch_following(cl, user_id, reported_following)
        return cache["following"]

    while True:

        show_menu(user)

        choice = ask("Select option")

        if choice == "1":
            show_profile(user)
            pause()

        elif choice == "2":
            url = getattr(user, "profile_pic_url", None)
            print()
            if url:
                ok("Profile picture:")
                print(f"{CYAN}{url}{RESET}")
            else:
                warn("Profile picture unavailable.")
            pause()

        elif choice == "3":
            show_posts(get_posts())
            pause()

        elif choice == "4":
            show_user_list(get_followers(), "FOLLOWERS", reported_followers)
            pause()

        elif choice == "5":
            show_user_list(get_following(), "FOLLOWING", reported_following)
            pause()

        elif choice == "6":
            open_profile(user.username)
            pause()

        elif choice == "7":
            print()
            warn("Full export may take time for large accounts.")
            full_export(cl, user, get_posts(), get_followers(), get_following())
            pause()

        elif choice == "8":
            show_profile(user)
            posts = get_posts()
            followers = get_followers()
            following = get_following()
            show_posts(posts)
            show_user_list(followers, "FOLLOWERS", reported_followers)
            show_user_list(following, "FOLLOWING", reported_following)
            pause()

        elif choice == "0":
            print()
            print(gradient_text("  ◆ Goodbye! ◆"))
            print()
            break

        else:
            err("Invalid option.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Interrupted.{RESET}")

    except Exception as e:
        print(f"\n{RED}[✗] Fatal error:{RESET}")
        print(str(e))
