# Kazushige Matsuda personal website

Static personal academic website for GitHub Pages or any simple web host.

## Edit content

- Main page: `index.html`
- Styles: `styles.css`
- Small interactions: `script.js`
- Profile image: `assets/profile.png`
- Publications data: `data/publications.json`
- CV source: `cv.qmd`
- Generated CV PDF: `assets/cv.pdf`

## Sync publications and CV

Edit `data/publications.json`, then run:

```sh
python3 scripts/build_site.py
```

This updates both the website publication sections and `cv.qmd` from the same source data.

The CV link on the website points to `assets/cv.pdf`. If Quarto is installed locally, render it with:

```sh
quarto render cv.qmd --to pdf
mkdir -p assets
mv cv.pdf assets/cv.pdf
```

On GitHub, `.github/workflows/build-cv.yml` renders the PDF automatically when the CV source or publication data changes.
