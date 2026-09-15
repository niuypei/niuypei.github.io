#!/usr/bin/env python3
"""Build a static Minimal Light homepage using only the Python standard library."""

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def publication_date(paper):
    value = paper.get("publication_date", str(paper["year"]))
    if not re.fullmatch(r"\d{4}(?:-\d{2}(?:-\d{2})?)?", value):
        raise ValueError("Publication date must use YYYY, YYYY-MM, or YYYY-MM-DD")
    parts = [int(part) for part in value.split("-")]
    parts += [1] * (3 - len(parts))
    result = date(*parts)
    if result.year != paper["year"]:
        raise ValueError("Publication date must match the bibliographic year: " + paper["id"])
    return result


def publication_sort_key(paper, name):
    return (not paper.get("pinned", False), paper["authors"][0] != name, -publication_date(paper).toordinal())


def escape(value):
    return html.escape(str(value), quote=True)


def link(url, label, **attributes):
    url = re.sub(r"[\t\r\n]", "", url).strip()
    if not url or any(ord(char) < 32 for char in url) or urlsplit(url).scheme.lower() not in ("", "https", "http", "mailto"):
        raise ValueError("Invalid content link: {!r}".format(url))
    extra = "".join(' {}="{}"'.format(k.rstrip("_").replace("_", "-"), escape(v)) for k, v in attributes.items())
    return '<a href="{}"{}>{}</a>'.format(escape(url), extra, escape(label))


def section(section_id, title, body):
    return '<section id="{0}" class="content-section" aria-labelledby="{0}-title"><h2 id="{0}-title">{1}</h2>{2}</section>'.format(section_id, escape(title), body)


def bibtex(paper):
    fields = {
        "title": "{{{}}}".format(paper["title"]),
        "author": " and ".join(paper["authors"]),
        "year": paper["year"],
    }
    if paper["type"] != "preprint":
        fields["journal" if paper["type"] == "journal" else "booktitle"] = paper["venue"]
    else:
        for field in ("eprint", "archivePrefix", "primaryClass"):
            if paper.get(field):
                fields[field] = paper[field]
    for field in ("volume", "number", "pages", "doi", "publisher"):
        if paper.get(field):
            fields[field] = paper[field]
    if paper.get("url"):
        fields["url"] = paper["url"]
    entries = ["  {} = {{{}}}".format(key, value) for key, value in fields.items()]
    kind = {"journal": "article", "conference": "inproceedings", "preprint": "misc"}[paper["type"]]
    return "@{}{{{},\n{}\n}}".format(kind, paper["id"], ",\n".join(entries))


def render_paper(paper, name):
    authors = ", ".join("<strong>{}</strong>".format(escape(a)) if a == name else escape(a) for a in paper["authors"])
    title = escape(paper["title"])
    resources = "".join(link(item["url"], item["label"], aria_label="{}: {}".format(item["label"], paper["title"])) for item in paper.get("links", []))
    resources += '<details class="citation"><summary aria-label="BibTeX: {}">BibTeX</summary><pre><code>{}</code></pre></details>'.format(escape(paper["title"]), escape(bibtex(paper)))
    award = paper.get("award")
    award_note = '<p class="publication-award">{}</p>'.format(link(award["url"], "{} {}".format(award["year"], award["label"]))) if award else ""
    return '''<li><article id="{id}" class="publication" aria-labelledby="{id}-title">
      <div class="publication-meta"><span class="venue-tag">{short_venue}</span><span class="publication-year">{display_year}</span></div>
      <div class="publication-body"><h4 id="{id}-title" class="publication-title">{title}</h4>
      <p class="authors">{authors}</p><p class="venue"><em>{citation}</em></p>
{award_note}
      <div class="paper-links">{resources}</div></div>
    </article></li>'''.format(id=escape(paper["id"]), short_venue=escape(paper["short_venue"]), display_year=escape(paper.get("display_year", paper["year"])), title=title, authors=authors, citation=escape(paper["citation"]), award_note=award_note, resources=resources)


def build():
    profile = json.loads((ROOT / "content/profile.json").read_text())
    papers = json.loads((ROOT / "content/publications.json").read_text())
    ids = set()
    for paper in papers:
        if not re.fullmatch(r"[a-z0-9-]+", paper["id"]) or paper["id"] in ids:
            raise ValueError("Invalid or repeated publication id")
        ids.add(paper["id"])
        if paper["type"] not in ("journal", "conference", "preprint"):
            raise ValueError("Invalid publication type")
        if profile["name"] not in paper["authors"]:
            raise ValueError("Profile author missing from publication: " + paper["id"])
        if not isinstance(paper["year"], int):
            raise ValueError("Publication year must be an integer")
        publication_date(paper)

    sections = [("about", "About"), ("research", "Research")]
    profile_links = []
    if profile.get("github"):
        profile_links.append(link(profile["github"], "GitHub"))
    if profile.get("cv"):
        profile_links.append(link(profile["cv"], profile.get("cv_label", "CV")))
    for item in profile.get("academic_links", []):
        profile_links.append(link(item["url"], item["label"]))

    publications = ""
    if papers:
        sections.append(("publications", "Publications"))
        groups = []
        for kind, label in (("preprint", "Preprints"), ("journal", "Journal articles"), ("conference", "Conference papers")):
            group = sorted((p for p in papers if p["type"] == kind), key=lambda p: publication_sort_key(p, profile["name"]))
            if group:
                groups.append('<h3 class="publication-group">{}</h3><ol class="bibliography">{}</ol>'.format(label, "".join(render_paper(p, profile["name"]) for p in group)))
        publications = '<section id="publications" class="content-section" aria-labelledby="publications-title"><div class="section-heading"><h2 id="publications-title">Publications</h2><a href="assets/files/publications.bib" download>Download BibTeX</a></div>{}</section>'.format("".join(groups))

    education = ""
    if profile.get("education"):
        sections.append(("education", "Education"))
        items = []
        for record in profile["education"]:
            institution = link(record["url"], record["institution"]) if record.get("url") else escape(record["institution"])
            detail = '<p class="education-detail">{}</p>'.format(escape(record["detail"])) if record.get("detail") else ""
            items.append('<li><span class="dates">{}</span><div><p><strong>{}</strong></p><p>{}</p>{}</div></li>'.format(escape(record["dates"]), escape(record["degree"]), institution, detail))
        education = section("education", "Education", '<ul class="education-list">{}</ul>'.format("".join(items)))

    projects = ""
    if profile.get("projects"):
        sections.append(("projects", "Open Source"))
        items = []
        for project in profile["projects"]:
            links = "".join(link(item["url"], item["label"]) for item in project.get("links", []))
            contributions = "".join('<li>{}</li>'.format(link(item["url"], item["label"])) for item in project.get("contributions", []))
            items.append('<article><h3 class="project-title">{}</h3><p>{}</p><div class="project-links">{}</div><ul class="project-contributions">{}</ul></article>'.format(escape(project["name"]), escape(project["description"]), links, contributions))
        projects = section("projects", "Open Source", "".join(items))

    awards = ""
    paper_awards = sorted((p for p in papers if p.get("award")), key=lambda p: -p["award"]["year"])
    if profile.get("awards") or paper_awards:
        sections.append(("awards", "Honors"))
        award_items = ["<li>{} — {} · {}</li>".format(link(p["award"]["url"], p["award"]["label"]), escape(p["title"]), escape(p["award"]["year"])) for p in paper_awards]
        award_items.extend('<li>{}</li>'.format(escape(item)) for item in profile.get("awards", []))
        awards = section("awards", "Honors & Awards", '<ul class="award-list">{}</ul>'.format("".join(award_items)))

    portrait = '<img class="portrait" src="{}" alt="{}" width="132" height="132">'.format(escape(profile["portrait"]), escape(profile["name"])) if profile.get("portrait") else ""
    email = link("mailto:" + profile["email"], profile["email"], class_="email") if profile.get("email") else ""
    substitutions = {
        "page_title": escape(profile["name"] + " | " + profile["focus"]),
        "description": escape(profile["description"]),
        "canonical": escape(profile["site_url"]),
        "name": escape(profile["name"]),
        "focus": escape(profile["focus"]),
        "portrait": portrait,
        "email": email,
        "profile_links": "".join(profile_links),
        "navigation": "".join(link("#" + target, label) for target, label in sections),
        "about": "".join('<p>{}</p>'.format(escape(paragraph)) for paragraph in profile["about"]),
        "research_interests": "".join('<li>{}</li>'.format(escape(item)) for item in profile["research_interests"]),
        "publications": publications,
        "education": education,
        "projects": projects,
        "awards": awards,
    }
    outputs = {ROOT / "index.html": Template((ROOT / "templates/index.html").read_text()).substitute(substitutions)}
    if papers:
        outputs[ROOT / "assets/files/publications.bib"] = "\n\n".join(bibtex(p) for p in papers) + "\n"
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files are up to date without writing")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, text in outputs.items() if not path.exists() or path.read_text() != text]
        if stale:
            raise SystemExit("Run python3 scripts/build.py to update: " + ", ".join(stale))
        print("Generated files are up to date.")
    else:
        for path, text in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        print("Built {} static file(s).".format(len(outputs)))
