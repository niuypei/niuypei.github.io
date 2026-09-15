# Yipei Niu · Academic Homepage

A static personal academic homepage based on [Minimal Light](https://github.com/yaoyao-liu/minimal-light). The site keeps the template's serif typography, blue academic headings, and profile sidebar.

## Update content

- `content/profile.json`: biography, research interests, contact links, education, projects, and honors.
- `content/publications.json`: publications, full author lists, venues, publication dates, and resource links.
- `assets/files/`: the generated bibliography and all four original slide PDFs. Paper full-text PDFs are not stored locally.
- `templates/index.html`: page structure.
- `assets/css/site.css`: local layout and style adjustments.

The generated `index.html` works without JavaScript or a server-side runtime. Build using Python 3.9 or later; no packages need to be installed:

```sh
python3 scripts/build.py
python3 scripts/check_site.py
```

Commit the updated source data together with the generated `index.html` and bibliography. Do not edit `index.html` directly; rebuilding would replace those edits.

## Preview

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Visit [http://localhost:8000](http://localhost:8000). Stop the server with Ctrl+C.

## GitHub Pages

This repository is a plain static site. GitHub Pages can publish the root directory of `main` using **Settings → Pages → Build and deployment → Deploy from a branch**. The `.nojekyll` file skips Jekyll processing. No build service, Node installation, or Ruby environment is needed to serve the committed output.

The canonical URL is configured in `content/profile.json`. If the site moves, update that field and rebuild. Verify the repository's Pages configuration before publishing changes.

## Publications

Paper titles are plain text in both Publications and Honors & Awards. Use the resource buttons for paper, Slides, and BibTeX access; award labels link to the official award announcement.

Each entry has a stable `id`, `type` (`journal`, `conference`, or `preprint`), full `authors`, `venue`, `short_venue`, integer `year`, formatted `citation`, canonical `url`, and `links` with `label`/`url` pairs. For papers with slides, `local_slides` records the preserved local archive path; it is not used by the generator. The visible Slides button is configured separately in `links`. Optional BibTeX fields include `doi`, `volume`, `number`, `pages`, and `publisher`. Preprints use `eprint`, `archivePrefix`, and optionally `primaryClass`, and export as `@misc`.

When a conference's event year differs from the proceedings publication year, use `display_year` for the event and `year` for the bibliography. Keep conference papers and their extended journal versions as separate records. The generator emphasizes Yipei Niu in author lists and produces downloadable and expandable BibTeX.

At the owner's request, **Demystifying the Cost of Serverless Computing: Towards a Win-Win Deal** (`serverless-cost-tpds-2024`) has `pinned: true` in `content/publications.json`, placing it first within Journal articles. The remaining papers in each publication type keep Yipei Niu's first-author papers ahead of other papers, with each group ordered newest first. Author lists, award information, and resource links retain their existing content.

The optional `publication_date` accepts `YYYY`, `YYYY-MM`, or `YYYY-MM-DD` at the source's actual precision, using the final issue/proceedings date or arXiv submission date. It must match `year`; `display_year` only controls the visible year label. Missing dates fall back to `year`, with unknown months/days treated as the start of the period for sorting.

An optional publication `award` object contains `label`, integer `year`, and an official `url`. It generates both the paper's award badge and an entry in Honors & Awards, so the same award need not be duplicated in `profile.json`. The 2024 IEEE TPDS Best Paper Award is documented in [the official-source verification record](docs/best-paper-award-2024.json).

Paper entry points use the actual official host: IEEE Xplore for IEEE publications, Springer for the two Springer publications, USENIX for ATC, and arXiv for the preprint. Buttons pointing to publisher article pages use the publisher name; `PDF` is reserved for an official paper PDF URL. Paper full-text links do not use author-hosted copies or local files.

Preserve all four original slide PDFs locally. Slides buttons prefer an official URL: ATC uses the USENIX Slides link, while INFOCOM 2015, 2017, and 2018 use their original local slide files because no official Slides URL has been verified. Keep the local ATC slides as an archive even though its visible button uses USENIX. The current check expects 12 publications, 12 BibTeX entries, and 9 local resource references, including the three local Slides links.

Empty sections are hidden. Add only verified personal records; template sample content is not used.

## Academic profile and sources

Education and honors were updated from the owner-provided resume on 2026-09-15. The owner explicitly selected the tagline AI Infra Engineer. Keep other homepage content focused on academic information: do not add employers, further job details, employment history, private contact details, or a complete resume download. The source resume is kept outside this repository. Award and scholarship sponsor names explicitly supplied by the owner are permitted in honors and do not imply employment.

The Google Scholar profile link has been removed from the homepage at the owner's request. Direct access to its publication list returned HTTP 429 during this update, so a complete Scholar comparison remains pending. The 12 current entries were checked against DBLP and publisher/arXiv records; see [the update record](docs/publication-update-2026-09-15.json) for the four additions and their sources.

## Sources and licenses

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [the academic redesign plan](docs/academic-homepage-redesign-plan.md). Fonts are hosted locally. The site does not load external analytics or icon libraries.
