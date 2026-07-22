# Web Site Worklog

Last updated: 2026-07-23

## Project

- Repository: `kmatsuda723/kmatsuda723.github.io`
- Local path: `/Users/kmatsuda/Documents/kazumatsuda.github.io`
- Public URL: <https://kmatsuda723.github.io/>
- GitHub Pages source: `main` branch, repository root

## Design Direction

- Built as a one-page personal academic website for a researcher.
- Style direction: Minimal Light / Academic Pages-inspired, but not a direct copy of another site.
- The page is intentionally minimal:
  - no top header or navigation bar
  - no repeated contact section at the bottom
  - no "Back to top" link
  - no repeated research interests in the sidebar
  - no duplicate paper buttons when the paper title already links out

## Current Homepage Structure

- Left column:
  - profile photo
  - name
  - email
  - CV link
- Main column:
  - Profile
  - Working Papers
  - Publications
  - Research in Progress

The Profile section currently uses this research description:

> I study higher education systems as institutions that govern the creation, embodiment, and allocation of knowledge, and how these mechanisms affect macroeconomic productivity.

Education information that was formerly in the left column was folded into the Profile section in natural English.

## Content Sources

- The old Google Sites page was used as a content reference:
  - <https://sites.google.com/view/kmatsuda>
- The old Google Sites page now points visitors to the new site:
  - <https://kmatsuda723.github.io/>
- The Google Docs CV was used as the reference for the CV contents:
  - `https://docs.google.com/document/d/1T2rbT7WUX3Q8B1uNR4nVDJ2wXpMG-qlX5laKw-EmkTM/edit?tab=t.0`

## CV Workflow

The site is set up to move away from a Google Docs CV and use a repository-based CV.

- CV source: `cv.qmd`
- Generated PDF: `assets/cv.pdf`
- Shared publication data: `data/publications.json`
- Build script: `scripts/build_site.py`
- GitHub Actions workflow: `.github/workflows/build-cv.yml`

The intended workflow is:

1. Edit `data/publications.json` for publication and working paper updates.
2. Run the build script to regenerate synced site/CV content when needed.
3. Commit and push the changes.
4. GitHub Actions renders `cv.qmd` to `assets/cv.pdf`.

This keeps the homepage publication list and the CV publication list synchronized from the same data source.

## Profile Photo Notes

Several changes were made to avoid darkening the profile photo:

- CSS filter/opacity effects were removed.
- Possible overlay/background darkening was considered and avoided.
- The photo was converted to untagged sRGB.
- The photo was also converted to PNG and is currently stored as:
  - `assets/profile.png`

If the image still appears darker than expected, the remaining likely causes are browser color management, the source image itself, or display differences rather than an intentional CSS darkening effect.

## Publication Display Notes

- Journal names on the homepage should be written out rather than abbreviated where requested.
- In particular, the homepage uses:
  - `American Economic Journal: Macroeconomics`
- Paper titles are clickable when a paper URL exists.
- Separate `Paper` / `Journal` buttons were removed because they duplicated the title links.

## GitHub Pages and Search Visibility

- The site is published through GitHub Pages at:
  - <https://kmatsuda723.github.io/>
- GitHub Pages deployment was confirmed as successful after the latest profile text update.
- Google search visibility is not immediate. The site can appear in search results after Google discovers and indexes it, but timing is controlled by Google.
- Helpful steps for search visibility:
  - keep the old Google Sites page linking to the new site
  - keep the homepage text clear and crawlable
  - optionally use Google Search Console later to request indexing

## Recent Commit History

Recent relevant commits at the time of this note:

- `11aeb32` Update profile research description
- `611a599` Build CV PDF
- `eae51d7` Use full AEJ journal name on homepage
- `d2332a4` Remove back to top footer link
- `ab3508a` Expand CV with Google Docs content
- `69b82bb` Add synced CV source and publication data
- `0b09b37` Remove sidebar affiliation text
- `2b9623c` Use PNG profile photo
- `9108dd8` Convert profile photo to untagged sRGB
- `c61dd9b` Remove profile photo filter

## Useful Commands

Check local status:

```sh
git status --short --branch
```

Regenerate homepage/CV source from the publication data:

```sh
python3 scripts/build_site.py
```

Commit and push updates:

```sh
git add .
git commit -m "Update site"
git push
```

Check GitHub Pages status:

```sh
gh api repos/kmatsuda723/kmatsuda723.github.io/pages
```
