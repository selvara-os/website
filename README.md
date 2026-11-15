# SelvaraOS website

Static website for SelvaraOS, published at https://selvara-os.github.io/website/.
No JavaScript, no cookies, no analytics, nothing loaded from other servers.

## Writing a news post

1. Open the `news` folder on GitHub and click **Add file → Create new file**.
2. Name it `YYYY-MM-DD-short-name.md`, for example `2026-11-20-dev-beta-1.md`.
   The part after the date becomes the address: `news/dev-beta-1.html`.
3. Copy the top block from `news/_template.md`, fill it in and write the post below it in Markdown.
4. Commit. The site rebuilds and goes online by itself in about a minute (see the **Actions** tab).

Images go in `news/img/` (**Add file → Upload files**). WebP or JPEG, about 1600 px wide.

Fields at the top of a post:

| Field | Required | Notes |
|---|---|---|
| `title` | yes | |
| `date` | yes | `2026-11-20` |
| `category` | yes | `Release`, `Announcement`, `Behind the scenes` or `Changelog` |
| `author` | no | defaults to `SelvaraOS team` |
| `cover` | no | `img/file.webp`, shown at the top of the post and in the news list |
| `cover_alt` | no | description of the cover image |
| `summary` | no | shown in the lists and the feed; defaults to the first paragraph |
| `draft` | no | `draft: true` keeps the post offline |

If something is wrong (a missing field, a misspelled category, an image that doesn't exist),
the build stops and the Actions tab shows a message that says exactly which file and what to fix.
The live site stays as it was until the error is fixed.

## Adding screenshots

Screenshots live in `screenshots/`, sorted by theme and by the day they were taken:

```
screenshots/
  Dark/
    2026-11-15/
      01-desktop.png
      02-launcher.png
  Light/
    2026-11-15/
      01-desktop.png
```

- Upload with **Add file → Upload files** into the right `Dark/<date>` or `Light/<date>` folder. PNG, JPEG or WebP, any size.
- The date folder (`YYYY-MM-DD`) is the day the screenshots were taken. It is shown on the page under every screenshot, newest day first.
- Inside a day they appear in file-name order, so start names with a number: `01-desktop.png`, `02-search.png`.
- The caption comes from the name: `03-control-center.png` is shown as "Control Center". Use English words separated by dashes.
- To remove a screenshot, delete its file.
- Commit, and the Screenshots page updates by itself in about a minute. A wrong folder name or a broken image stops the build with a message that says which file to fix.

## Building locally

```
pip install -r requirements.txt
python build.py
```

The result is written to `_site/`.

## Licence

Code: GPL-3.0-or-later. Wallpapers: CC-BY-SA-4.0.
