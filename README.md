# Daily Quran Wallpaper

A small Python app that picks a meaningful Quran ayah every day, renders it onto an
**iPhone 14 Pro–sized** (1179 × 2556) image with Arabic + English (Sahih International)
in gold on a near-black background, and publishes it to a stable GitHub Pages URL.

The image at the URL changes daily; the URL itself never does.

```
https://raw.githubusercontent.com/<your-username>/<repo-name>/refs/heads/main/docs/wallpaper.png
```

---

## How it works

1. A GitHub Actions workflow runs every day at **05:00 UTC** (and on demand).
2. The Python app deterministically selects today's ayah from a curated list of
   ~200 significant verses (Ayat al-Kursi, last 2 of Baqarah, Al-Fatiha, Al-Ikhlas,
   Mu'awwidhatayn, well-known verses from Yasin, Ar-Rahman, Al-Mulk, etc.).
3. It fetches the Arabic (Uthmani) and English (Sahih International) text from
   [AlQuran.cloud](https://alquran.cloud/api).
4. It renders both onto a 1179×2556 PNG with a subtle dark gradient and a gold
   double border, then writes the result to `docs/wallpaper.png`.
5. The workflow commits and pushes; GitHub Pages serves the new image at the same URL.

---

## Repo layout

```
src/
  ayahs.py     # curated ayah list + date-based selector
  fetch.py     # AlQuran.cloud client
  render.py    # Pillow renderer (Arabic shaping + RTL, gold styling)
  style.py     # colors, sizes, fonts, safe-area constants
  main.py      # CLI entry point
assets/fonts/  # Amiri (Arabic) + Cormorant Garamond (Latin) — downloaded by script
docs/          # served by GitHub Pages
  wallpaper.png
  wallpaper.json
  index.html
.github/workflows/daily.yml
scripts/download_fonts.py
tests/
```

---

## One-time GitHub setup

You manage the GitHub side manually. Steps:

1. **Create a new GitHub repo** and push this codebase to it.
2. **Enable GitHub Pages**:
   - Repo **Settings → Pages**
   - **Source**: *Deploy from a branch*
   - **Branch**: `main`, **folder**: `/docs`
   - Save. After the first successful workflow run, your URL will be
     `https://<your-username>.github.io/<repo-name>/wallpaper.png`.
3. **Allow Actions to push back to the repo**:
   - **Settings → Actions → General → Workflow permissions**
   - Choose **Read and write permissions** → Save.
4. **Trigger the first run**:
   - **Actions → Daily Quran Wallpaper → Run workflow**.
   - Wait ~1 minute, then visit your Pages URL.

---

## Local development

```powershell
# 1. Create venv & install deps
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Download the fonts (one-time)
python scripts/download_fonts.py

# 3. Generate today's wallpaper into docs/
python -m src.main

# Useful flags:
python -m src.main --ayah 2:255 --preview          # render a specific verse and open it
python -m src.main --date 2026-12-25               # render the verse that would be picked on a given date
python -m src.main --out preview.png --preview     # write somewhere other than docs/

# Run tests
pip install pytest
pytest
```

---

## iOS Shortcut: auto-set the wallpaper every morning

You only need to set this up once on your iPhone.

### 1. Build the shortcut

Open the **Shortcuts** app → **+** to create a new shortcut, then add these actions in order:

1. **Text** → enter your URL with a cache-buster placeholder, e.g.
   `https://<your-username>.github.io/<repo-name>/wallpaper.png?t=`
2. **Current Date**
3. **Format Date**
   - Date Format: **Custom**
   - Format String: `yyyyMMddHHmm`
4. **Combine Text** (or just chain via "Text" + magic variables): combine the URL text
   with the formatted date so the final string looks like
   `…/wallpaper.png?t=202605011234`.
5. **Get Contents of URL** → URL = the combined text from step 4.
6. **Set Wallpaper**
   - Picture: *Contents of URL*
   - Show Preview: **Off**
   - Set: **Lock Screen** (or both Lock + Home)

Name it something like **"Daily Quran Wallpaper"**.

> The `?t=…` query parameter is ignored by GitHub Pages but forces iOS to bypass its
> aggressive image cache, so you actually get the new image.

### 2. Schedule it

In **Shortcuts**, switch to the **Automation** tab → **+** → **Create Personal Automation**:

- **Time of Day** → e.g. **06:00 AM**, **Daily**.
- **Next** → add **Run Shortcut** → pick **Daily Quran Wallpaper**.
- Toggle **Run Immediately** **on** (so it doesn't ask you each morning).
- **Done**.

That's it — every morning your lock screen will refresh with the new ayah.

---

## Customizing

- **Change the gold shade or background**: edit constants in
  [`src/style.py`](src/style.py).
- **Add or remove ayahs**: edit `SIGNIFICANT_AYAHS` in
  [`src/ayahs.py`](src/ayahs.py).
- **Change the schedule**: edit the `cron` line in
  [`.github/workflows/daily.yml`](.github/workflows/daily.yml).
- **Use a different translation**: change `ENGLISH_EDITION` in
  [`src/fetch.py`](src/fetch.py) (e.g. `en.pickthall`, `en.yusufali`).

---

## Credits & licensing

- **Quran text + translation**: [AlQuran.cloud](https://alquran.cloud/api) (free API).
- **Amiri** font: © Khaled Hosny — SIL Open Font License 1.1.
- **Cormorant Garamond** font: © Christian Thalmann — SIL Open Font License 1.1.
- App code: do whatever you'd like with it.

## To-Do
- [ ] Change arabic font to use harakat
- [ ] Fix sizing to fit within widgets
- [ ] Header generation for security when requesting image (maybe)

## Future Development
- [ ] Creating a interface / mobile application to handle user creation and customised wallpaper generation
- [ ] Wallpaper generation for different domains: Bible quotes, Inspirational Quotes, Countdown
- [ ] Subscription method for different fonts, colours, and background (essentially more customisation)
- [ ] Free Palestine flag in corner - money to go to charity
