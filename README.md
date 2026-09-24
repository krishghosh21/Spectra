<div align="center">

```
██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗██████╔╝███████║██╔████╔██║
██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
```

# Instagram Profile Tool

**A fast, beautiful terminal toolkit for viewing and exporting Instagram profile data through the mobile API.**

Profile details · Posts · Followers · Following · One-command full export

<br>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![instagrapi](https://img.shields.io/badge/powered%20by-instagrapi-E1306C?style=for-the-badge&logo=instagram&logoColor=white)](https://github.com/subzeroid/instagrapi)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-833AB4?style=for-the-badge)](#-requirements)
[![License](https://img.shields.io/badge/license-MIT-FCB045?style=for-the-badge)](#-license)

[![Terminal UI](https://img.shields.io/badge/UI-truecolor%20terminal-FD1D1D?style=flat-square)](#-features)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)](#-roadmap)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-4ADE80?style=flat-square)](#-contributing)

<br>

[Features](#-features) ·
[Installation](#-installation) ·
[Usage](#-usage) ·
[Output](#-export-output) ·
[Configuration](#-configuration) ·
[Troubleshooting](#-troubleshooting) ·
[Disclaimer](#-legal-disclaimer)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Preview](#-preview)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Getting Your Session ID](#-getting-your-session-id)
- [Usage](#-usage)
- [Menu Reference](#-menu-reference)
- [Export Output](#-export-output)
- [Configuration](#-configuration)
- [Understanding the Terminal UI](#-understanding-the-terminal-ui)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Security & Privacy](#-security--privacy)
- [Legal Disclaimer](#-legal-disclaimer)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## ✨ Overview

**Instagram Profile Tool** is an interactive command-line application built on top of [`instagrapi`](https://github.com/subzeroid/instagrapi). It authenticates with an existing Instagram session, looks up a profile, and lets you browse or export everything the mobile API exposes for it: profile details, posts with permalinks, follower and following lists, and downloadable media.

It is designed to feel good to use:

- A **gradient ASCII banner** and a modern **truecolor** interface
- **Live progress bars** and spinners for every long-running operation
- **Smart caching**, so data is only fetched once per session
- **Built-in integrity checks** that compare what was fetched against what Instagram reports
- A **complete structured export** (JSON + media) in a single menu action

> [!IMPORTANT]
> This tool is intended for use with **your own account** or an account you are **explicitly authorized** to use. Please read the [Legal Disclaimer](#-legal-disclaimer) before use.

---

## 🚀 Features

| | Feature | Description |
|---|---|---|
| 👤 | **Profile inspector** | Username, full name, user ID, bio, external link, post/follower/following counts, and verified / private / business badges |
| 🖼️ | **Profile picture** | View the direct URL or download the image |
| 📸 | **Post browser** | Every post with ID, media type, likes, comments, date, permalink, and caption preview |
| 👥 | **Followers list** | Paginated fetch with a live progress bar and a formatted table |
| ➕ | **Following list** | Same as above for accounts the profile follows |
| 📦 | **Full export** | One action writes profile, followers, following, posts, images, and videos to disk |
| ✅ | **Integrity check** | Compares fetched counts against the counts the profile reports, and flags mismatches |
| 🎨 | **Rich terminal UI** | Truecolor gradients, rounded boxes, spinners, progress bars, ANSI-aware alignment |
| 🧠 | **Session cache** | Followers, following, and posts are fetched once and reused across menu options |
| 🛡️ | **Compatibility fallback** | Automatically falls back to `user_medias`, `user_followers_v1`, and `user_following_v1` if the `iter_*` helpers are missing in your `instagrapi` version |
| 🪟 | **Cross-platform** | Works on Windows 10+, macOS, and Linux |

---

## 🖥️ Preview

<!--
Optional: add your own screenshots to an /assets folder and uncomment.

<p align="center">
  <img src="assets/menu.png" width="48%" alt="Main menu">
  <img src="assets/followers.png" width="48%" alt="Followers table">
</p>
-->

**Main menu**

```
╭────────────────── MAIN MENU · @your_username ──────────────────╮
│ [1]  Profile information                                       │
│ [2]  Profile picture URL                                       │
│ [3]  All posts + links                                         │
│ [4]  All followers                                             │
│ [5]  All following                                             │
│ [6]  Open Instagram profile                                    │
│ [7]  Download ALL details                                      │
│ [8]  Full terminal report                                      │
├────────────────────────────────────────────────────────────────┤
│ [0]  Exit                                                      │
╰────────────────────────────────────────────────────────────────╯
```

**Live progress while fetching**

```
[*] Fetching followers using mobile API...
Followers  ████████████████████████░░░░  170/198   85.9%
```

**Followers table**

```
    #  USERNAME                       NAME                         FLAGS
────────────────────────────────────────────────────────────────────────────
    1  @example_user_one              Example One
    2  @example_user_two              Example Two                  ●
    3  @example_user_three            Example Three                ✔ ●
```

**Export summary**

```
╭──────────────────── EXPORT COMPLETED ────────────────────╮
│                    fetched / reported                    │
├──────────────────────────────────────────────────────────┤
│ Followers   170 / 198 ≠                                  │
│ Following   328 / 331 ≠                                  │
│ Posts       1 / 1 ✔                                      │
├──────────────────────────────────────────────────────────┤
│ Saved to instagram_export/your_username                  │
╰──────────────────────────────────────────────────────────╯
```

---

## 📋 Requirements

| Requirement | Details |
|---|---|
| **Python** | 3.9 or newer |
| **Packages** | `instagrapi`, `requests` |
| **Terminal** | A **truecolor (24-bit)** terminal for the full gradient experience |
| **Instagram account** | A valid, logged-in session (see [Getting Your Session ID](#-getting-your-session-id)) |

**Recommended terminals**

- Windows: Windows Terminal, VS Code integrated terminal
- macOS: iTerm2, Terminal.app, Warp, Kitty
- Linux: GNOME Terminal, Konsole, Alacritty, Kitty, xfce4-terminal, VS Code

> [!NOTE]
> The legacy Windows `cmd.exe` console does not render truecolor gradients correctly. Use Windows Terminal instead.

---

## 📦 Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/instagram-profile-tool.git
cd instagram-profile-tool
```

**2. (Recommended) Create a virtual environment**

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

`requirements.txt`

```text
instagrapi
requests
```

Or install directly:

```bash
pip install instagrapi requests
```

**4. Run**

```bash
python insta_tool.py
```

---

## 🔑 Getting Your Session ID

The tool authenticates with your Instagram **`sessionid`** cookie instead of asking for your password.

1. Log in to **[instagram.com](https://www.instagram.com)** in your desktop browser using your own account.
2. Open **Developer Tools** (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`).
3. Go to the **Application** tab (Chrome/Edge) or the **Storage** tab (Firefox).
4. Expand **Cookies** and select `https://www.instagram.com`.
5. Find the cookie named **`sessionid`** and copy its **Value**.
6. Paste it when the tool prompts you.

> [!WARNING]
> **Treat your `sessionid` like a password.** Anyone who has it can act as your account. Never share it, never paste it into an issue, and never commit it to Git. Logging out of Instagram in the browser invalidates it.

---

## 🎮 Usage

```bash
python insta_tool.py
```

**Flow**

1. The banner loads and the notice about authorized use is displayed.
2. Paste your `sessionid`. The tool validates it against the **mobile API** and prints the logged-in account.
3. Enter the Instagram **username** you want to inspect (the `@` is optional).
4. Pick actions from the **main menu**. Fetched data is cached, so opening followers twice does not re-download anything.

**Example session**

```text
❯ Enter sessionid: ********
✓ Session accepted
✓ Logged in as @your_username

❯ Enter Instagram username: your_username
✓ Profile found

❯ Select option: 7
[!] Full export may take time for large accounts.
[*] Export directory: instagram_export/your_username
[✓] profile.json saved
[✓] followers.json saved (170 fetched)
...
```

> [!NOTE]
> Private profiles can only be read if the authenticated account is already approved to view them. The tool does not and cannot bypass Instagram's access controls.

---

## 🧭 Menu Reference

| Key | Action | What it does |
|:---:|---|---|
| `1` | **Profile information** | Shows a formatted profile card with stats, badges, link, and wrapped biography |
| `2` | **Profile picture URL** | Prints the direct profile picture URL |
| `3` | **All posts + links** | Fetches every post and lists ID, type, likes, comments, date, permalink, and caption preview |
| `4` | **All followers** | Fetches followers with live progress and displays a table with flags |
| `5` | **All following** | Same as above for the following list |
| `6` | **Open Instagram profile** | Prints the profile URL and opens it in your default browser |
| `7` | **Download ALL details** | Runs the full export (see [Export Output](#-export-output)) |
| `8` | **Full terminal report** | Prints profile, posts, followers, and following in one go |
| `0` | **Exit** | Closes the tool |

---

## 📁 Export Output

Option **7** creates a folder per profile inside `instagram_export/`:

```text
instagram_export/
└── <username>/
    ├── profile.json              # Full profile object
    ├── profile_picture.jpg       # Downloaded profile picture
    ├── profile_picture_url.txt   # Direct picture URL
    ├── followers.json            # All fetched followers
    ├── following.json            # All fetched following
    ├── posts.json                # All fetched post metadata
    ├── data_summary.json         # Export report + integrity check
    └── posts/                    # Downloaded photos, videos, and album items
```

### `data_summary.json`

A machine-readable report of the export, including whether the fetched data matches what the profile reports:

```json
{
    "export_time": "2026-09-24T21:11:03.412881",
    "username": "your_username",
    "user_id": "1234567890",
    "reported_by_profile": {
        "followers": 198,
        "following": 331,
        "posts": 1
    },
    "actually_fetched": {
        "followers": 170,
        "following": 328,
        "posts": 1
    },
    "complete_match": {
        "followers": false,
        "following": false,
        "posts": true
    },
    "directory": "instagram_export/your_username"
}
```

### Supported media types

| Type | Value | Downloader |
|---|:---:|---|
| Photo | `1` | `photo_download` |
| Video / Reel | `2` | `video_download` |
| Album / Carousel | `8` | `album_download` |

---

## ⚙️ Configuration

All settings live in the **CONFIG** section at the top of `insta_tool.py`.

| Setting | Default | Description |
|---|:---:|---|
| `EXPORT_ROOT` | `Path("instagram_export")` | Base folder for all exports |
| `FOLLOWER_PAGE_SIZE` | `200` | Followers requested per API page |
| `FOLLOWING_PAGE_SIZE` | `200` | Following requested per API page |
| `POST_PAGE_SIZE` | `12` | Posts requested per API page |
| `FOLLOWER_LIMIT` | `0` | Max followers to fetch (`0` = all) |
| `FOLLOWING_LIMIT` | `0` | Max following to fetch (`0` = all) |
| `POST_LIMIT` | `0` | Max posts to fetch (`0` = all) |
| `BOX_WIDTH` | `68` | Width of the boxed UI elements |
| `ANIMATE` | `True` | Enables the banner reveal animation |

**Example: quick test with limited data**

```python
FOLLOWER_LIMIT = 50
FOLLOWING_LIMIT = 50
POST_LIMIT = 10
ANIMATE = False
```

### Customising the look

The banner gradient is controlled by `IG_STOPS`, a list of RGB colour stops:

```python
IG_STOPS = [
    (131, 58, 180),   # purple
    (225, 48, 108),   # pink
    (253, 29, 29),    # red
    (252, 176, 69),   # orange
]
```

Swap in any list of RGB tuples to create a different theme (for example neon cyan → violet, or a green "hacker" look).

---

## 🎨 Understanding the Terminal UI

### Flags column

| Symbol | Colour | Meaning |
|:---:|:---:|---|
| `✔` | Green | **Verified** account (blue tick) |
| `●` | Red | **Private** account |
| *(blank)* | | Public, non-verified account |

### Profile badges

| Badge | Meaning |
|---|---|
| `✔ VERIFIED` | Verified account |
| `● PRIVATE` / `● PUBLIC` | Account visibility |
| `◆ BUSINESS` | Business or professional account |

### Integrity marks (export summary)

| Mark | Meaning |
|:---:|---|
| `✔` | Fetched count exactly matches the profile-reported count |
| `≠` | Counts differ. See [Why don't the counts match?](#why-dont-the-counts-match) |

---

## 🛠️ Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `Authentication failed` | Expired or invalid `sessionid` | Log in to Instagram again, copy a fresh `sessionid` |
| `Mobile API validation failed` | Session works for public lookups but is rejected by private endpoints | Log out and back in on the web, then use the new `sessionid` |
| `Profile lookup failed` | Wrong username, account deleted, or temporary block | Double-check the username; wait a few minutes and retry |
| Fetch stops early / partial lists | Rate limiting or soft throttling | Wait a few minutes and retry; use smaller `*_PAGE_SIZE` values |
| `login_required` / challenge errors | Instagram flagged the session | Open Instagram in your browser, resolve any prompts, get a new `sessionid` |
| Gradients look wrong or plain | Terminal lacks truecolor | Use a modern terminal (see [Requirements](#-requirements)) |
| Boxes (▯) instead of emoji in names | Terminal font has no emoji glyphs | Install an emoji-capable font, e.g. *Noto Color Emoji* |
| Table columns shift on some rows | Emoji and fancy Unicode fonts have variable width | Cosmetic only; data is unaffected |
| `iter_user_*` attribute errors | Older/newer `instagrapi` version | The tool falls back automatically; otherwise run `pip install -U instagrapi` |
| Media download fails for a post | Deleted post, unsupported type, or temporary block | Failures are counted and reported; re-run the export |

### Why don't the counts match?

A `≠` next to followers or following is common and does not necessarily mean something went wrong. Typical reasons:

- **Deactivated, banned, or restricted accounts.** Instagram's headline count can include accounts the API no longer returns.
- **Pagination interruptions.** Rate limits can end a list early. Waiting and retrying often recovers the missing entries.
- **Count lag.** The number on the profile can be slightly stale compared to the live list.

If the mismatch is large, wait a few minutes and run the fetch again.

---

## ❓ FAQ

<details>
<summary><b>Do I need to enter my Instagram password?</b></summary>

No. The tool only asks for your `sessionid` cookie. Your password is never requested or stored.
</details>

<details>
<summary><b>Is my session ID saved anywhere?</b></summary>

No. It is kept in memory for the duration of the run only. It is not written to disk by this tool.
</details>

<details>
<summary><b>Can it access private profiles?</b></summary>

Only if the authenticated account already has permission to view them (for example, it is an approved follower). The tool does not bypass privacy settings.
</details>

<details>
<summary><b>Can my account get restricted?</b></summary>

Any automation against Instagram carries some risk, especially large fetches in a short time. Keep usage moderate, avoid running many exports back to back, and consider using the `*_LIMIT` settings.
</details>

<details>
<summary><b>How long does a full export take?</b></summary>

It depends on account size and network conditions. Small accounts finish in seconds; accounts with thousands of followers or many posts take longer, especially with media downloads.
</details>

<details>
<summary><b>Does it work on Windows?</b></summary>

Yes, on Windows 10 and newer. Use Windows Terminal for the best visuals.
</details>

<details>
<summary><b>Can I change the colours?</b></summary>

Yes. Edit `IG_STOPS` and the colour constants (`PINK`, `PURPLE`, `CYAN`, and so on) at the top of the script.
</details>

---

## 🗂️ Project Structure

```text
instagram-profile-tool/
├── insta_tool.py        # Main application
├── requirements.txt     # Python dependencies
├── README.md            # You are here
├── LICENSE              # License text
├── .gitignore           # Keeps exports and secrets out of Git
└── instagram_export/    # Generated at runtime (git-ignored)
```

**Recommended `.gitignore`**

```gitignore
# Exports (contain personal data)
instagram_export/

# Python
__pycache__/
*.pyc
venv/
.venv/

# Secrets and sessions
*.session
session*.json
.env
```

**Inside `insta_tool.py`**

| Section | Responsibility |
|---|---|
| CONFIG | User-adjustable limits and appearance |
| COLORS | Truecolor palette and gradient engine |
| TERMINAL HELPERS | Status lines, spinner, progress bar |
| BOXES / LAYOUT | ANSI-aware box drawing |
| BANNER | Gradient ASCII art |
| SERIALIZER | Converts `instagrapi` objects to JSON-safe data |
| SESSION | Authentication and mobile-API validation |
| PROFILE / POSTS / FOLLOWERS | Fetching and display |
| EXPORT | Full export and summary report |
| MENU / MAIN | Interactive loop with session cache |

---

## 🗺️ Roadmap

- [x] Gradient ASCII banner and truecolor UI
- [x] Progress bars and spinners
- [x] Session cache across menu options
- [x] Integrity check for exported counts
- [x] Automatic fallback for older/newer `instagrapi` versions
- [ ] Configurable request delay to reduce throttling
- [ ] Retry logic for interrupted follower/following fetches
- [ ] Diff mode: compare two exports (new / lost followers)
- [ ] CSV and HTML export formats
- [ ] Pager for long lists
- [ ] Command-line arguments for non-interactive use
- [ ] Optional session persistence in a secure local file
- [ ] Theme presets (neon, cyberpunk, mono)

Have an idea? [Open an issue](../../issues) and let's talk about it.

---

## 🤝 Contributing

Contributions are welcome.

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/amazing-idea`
3. **Commit** your changes: `git commit -m "Add amazing idea"`
4. **Push** the branch: `git push origin feature/amazing-idea`
5. **Open a Pull Request**

**Guidelines**

- Keep the code readable and consistent with the existing structure
- Test on at least one platform before submitting
- Never include real session IDs, exports, or personal data in commits, issues, or screenshots
- Describe what changed and why in your PR

**Bug reports** should include your Python version, OS, terminal, `instagrapi` version (`pip show instagrapi`), and the full error output with any sensitive values removed.

---

## 🔒 Security & Privacy

- Your `sessionid` grants full access to your account. **Never share it or commit it.**
- Exports may contain **personal data about other people** (usernames, names, profile details). Store them securely and do not publish them.
- If you believe a session ID has leaked, **log out** of Instagram everywhere and change your password.
- Do not attach exports or screenshots containing real user data to public issues or pull requests.

To report a security concern, please open a private security advisory on the repository rather than a public issue.

---

## ⚖️ Legal Disclaimer

This project is provided **for educational and personal-use purposes only**.

- It is **not affiliated with, authorized, maintained, sponsored, or endorsed by Instagram or Meta Platforms, Inc.** Instagram is a trademark of its respective owner.
- It relies on Instagram's **unofficial, private mobile API** through a third-party library. That API can change or break without notice, and using automated tools against Instagram may violate its **Terms of Use** and can lead to rate limits, temporary blocks, or account restrictions.
- Use this tool **only with accounts you own or are explicitly authorized to access**, and only to view or export data you have the right to access.
- You are solely responsible for how you use this software and for complying with all applicable laws and regulations, including privacy and data-protection laws such as GDPR and CCPA, and Instagram's own policies.
- The authors and contributors provide this software **"as is"**, without warranty of any kind, and accept **no liability** for any damages, account actions, or legal consequences arising from its use.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

```text
MIT License

Copyright (c) 2026 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgements

- **[instagrapi](https://github.com/subzeroid/instagrapi)** for the Instagram API client that powers this tool
- **[Requests](https://requests.readthedocs.io/)** for simple, reliable HTTP
- **[Shields.io](https://shields.io/)** for the badges

---

<div align="center">

**If this project helped you, consider giving it a ⭐**

Made with 💜 and a lot of terminal colours

[⬆ Back to top](#instagram-profile-tool)

</div>
