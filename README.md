# BSCS Website

Official website prototype for **Bocconi Students Commodities Society** with a Markdown-based publication workflow.

## Publish on GitHub Pages

1. Extract this ZIP on your computer.
2. Open your GitHub repository (`BocconiCommodities/web1.0`).
3. Upload **the contents of this folder** to the root of your repository, preserving `articles/` and `.github/workflows/`. Replace its old `index.html`.
4. Commit the files to `main`.
5. Leave **Settings → Pages → Deploy from a branch → main → /(root)** as configured.
6. In **Settings → Actions → General → Workflow permissions**, ensure **Read and write permissions** is selected, so the automatic publisher can update `index.html`. If you change it, save.
7. Check **Actions → Build articles and publish BSCS**. When complete, GitHub Pages serves the generated site.

## Add a new article

1. Open the `articles` folder on GitHub.
2. Choose **Add file → Create new file**, and name it `your-article-title.md` (lowercase letters and hyphens only).
3. Copy an existing article's structure, update the metadata and write your text in Markdown.
4. Set `demo: false` for a real article. Set `featured: true` only if you want it featured on Home.
5. Commit changes. GitHub Actions rebuilds the home page, category listing and reader pages automatically.

The latest three **other** articles appear on Home, sorted by `date`. Each category filters the same automatically generated list.

Each Markdown file needs this header:

```yaml
---
title: Example Article Title
category: Energy
date: 2026-10-22
author: Firstname Lastname
description: A short summary of the report.
image: https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1200
featured: false
demo: false
---

## Introduction
Your article text here.
```

Allowed categories: Mining & Metals, Energy, Agriculture, Shipping & Logistics, ESG, Physical Trading, Quant, Portfolio Management.

If you upload a new **PDF**, it will **not** convert automatically. Convert its content into Markdown first, and upload images separately if needed. This system intentionally uses Markdown files so BSCS articles can be displayed as responsive web pages. PDF support can be added later.

## Editing and local build

`template.html` contains the site layout and leadership content; **do not edit generated `index.html` to publish articles**.

```bash
pip install -r requirements.txt
python build.py
```

A single root `index.html` is generated with articles embedded, so the live website works on GitHub Pages without a backend. Images from external URLs require internet access.

## Demonstration content

The eight sample articles are fictional and contain prominent notices that they are **not BSCS research**. Delete their `.md` files when publishing real research if you no longer need them.
