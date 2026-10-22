# BSCS Website

Official website of **Bocconi Students Commodities Society (BSCS)**, hosted using GitHub Pages. The site publishes society research and events through Markdown and YAML files. GitHub Actions generates the HTML pages automatically.

## Website and repository

- Public website: https://bocconicommodities.github.io/web1.0/
- Repository: https://github.com/BocconiCommodities/web1.0
- GitHub Pages setting: **Deploy from a branch** → **main** → **/(root)**.
- Workflow: `.github/workflows/publish.yml` runs `build.py` after the configured pushes. Check the **Actions** tab for successful runs.

## File structure

```text
web1.0/
├── .github/workflows/publish.yml  # Automation; keep existing
├── articles/                       # One Markdown file per article
├── events/                         # One YAML file per event
│   └── bbva-research-metals-outlook.yml
├── assets/                         # Event images and other uploaded images
│   └── bbva-research-event.jpeg
├── featured.yml                    # Featured item selection
├── template.html                   # Website design and behavior
├── build.py                        # Generates publication pages
├── requirements.txt                # Python dependencies; keep existing
├── index.html                      # Generated website homepage
├── archive.html                    # Generated article archive
├── events.html                     # Generated event archive
└── README.md                       # This guide
```

**Do not manually edit `index.html`, `archive.html`, or `events.html` for permanent changes.** The build process regenerates them from `template.html` and the content files. For lasting design changes, update `template.html` and, where needed, `build.py`.

## Publish an article

1. On GitHub, open the `articles/` folder and select **Add file → Create new file**, or upload a Markdown file.
2. Name it using lowercase letters, digits and hyphens, for example `2026-copper-supply.md`.
3. Use this structure, with the YAML block at the beginning:

```markdown
---
title: "Understanding Copper Supply"
category: "Mining & Metals"
date: 2026-11-20
author: "Author Name"
description: "A short summary for the article card."
image: "assets/copper-cover.jpg"
demo: false
featured: false
---

## Introduction

Write the research article here in Markdown.

## Market drivers

Explain the key developments, evidence and sources.
```

4. If you reference an image, upload it to `assets/` and use the matching relative path. A public web image URL can also be used when appropriate.
5. Commit the changes. GitHub Actions runs the generator, and GitHub Pages publishes the regenerated site.

**Allowed categories:** `Mining & Metals`, `Energy`, `Agriculture`, `Shipping & Logistics`, `ESG`, `Physical Trading`, `Quant`, `Portfolio Management`. The spelling must match exactly.

All current example articles have `demo: true`; the generator excludes them. To publish a real article, use `demo: false`. With the first real article, the **Latest Articles** section appears on Home. Home shows up to three latest articles, and the main Articles section shows up to six. The full article archive is available via **View more articles** when applicable.

The `featured: true` field is retained as article metadata, but the **homepage featured slot is explicitly selected using `featured.yml`**.

## Add an event

1. Copy `events/bbva-research-metals-outlook.yml` as a model and create a separate `.yml` file for the new event.
2. Update each field. Example:

```yaml
slug: copper-market-panel
title: "Copper Market Panel"
date: 2026-12-05
dateLabel: "Saturday, 5 December 2026"
format: "Online · Google Meet"
time: "18:00 (CET)"
desc: "Discussion of copper market fundamentals with invited speakers."
image: "assets/copper-panel.jpg"
url: "https://example.com/registration"
```

3. Upload the matching event image to `assets/` and verify its path.
4. Replace the registration URL with the real one and commit the files.

The main Events section displays up to six events; the full listing is on the events archive page. Each event card opens the URL set in its event file. Events are currently sorted by their `date` field, newest first; they are not automatically removed after the event date.

## Choose Featured Event or Featured Article

Open `featured.yml` and select exactly one item:

**Featured event:**
```yaml
type: event
slug: bbva-research-metals-outlook
```

**Featured article:**
```yaml
type: article
slug: 2026-copper-supply
```

For articles, the slug is the Markdown filename **without `.md`**. For events, the slug must match the chosen event's filename **without `.yml`**. Make sure the target exists and, for articles, that it is not marked `demo: true`. Commit the change to rebuild the website.

## Updating the website design

To permanently change typography, colors, navigation, sections, or team links, edit `template.html`; change `build.py` only when modifying how content is processed. Then commit. Avoid editing the generated HTML pages as they will be overwritten by the next build.

## Troubleshooting

- **Old website or README appears instead of the site:** hard-refresh your browser (`Ctrl + Shift + R`) or open the public URL in a private window. Confirm GitHub Pages is serving from `main` / `/(root)`.
- **New article or event missing:** check GitHub **Actions** for a failed workflow, confirm metadata and file paths, and verify the event/article is not a demo.
- **Images missing:** check spelling, case and exact paths in `assets/`.
- **Workflow fails:** open the failed Actions run to read the specific error. Do not delete `.github/workflows/publish.yml`.

## Current initial content

- Event: **Metals & Commodities Outlook with BBVA Research**, Tuesday 10 November 2026, online in the evening (CET), exact time to be confirmed. Registration: https://lnkd.in/e2QwQfmc
- The supplied event graphic may still carry the previous BMCS branding; replace the image in `assets/` once the updated BSCS graphic is available.
- The example research articles remain in `articles/` for reference, but are hidden because they are marked `demo: true`.
