#!/usr/bin/env python3
"""Check generated content, internal links, assets, and publication completeness."""

import json
import re
import subprocess
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.references = []
        self.papers = []
        self.citations = 0
        self.lang = None
        self.title = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "title":
            self.title = True
        if tag == "article" and "publication" in attrs.get("class", "").split():
            self.papers.append(attrs.get("id"))
        if tag == "details" and "citation" in attrs.get("class", "").split():
            self.citations += 1
        if tag == "img" and not attrs.get("alt"):
            raise ValueError("Image missing a meaningful alt attribute")
        for attribute in ("src", "href"):
            if attribute in attrs:
                self.links.append(attrs[attribute])
        for attribute in ("aria-labelledby", "aria-describedby"):
            self.references.extend(attrs.get(attribute, "").split())


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"], check=True)
    markup = (ROOT / "index.html").read_text()
    publications = json.loads((ROOT / "content/publications.json").read_text())
    local_slides = set()
    for paper in publications:
        if paper.get("local_slides"):
            slide_url = urlsplit(paper["local_slides"])
            assert not slide_url.scheme and not slide_url.netloc, "Slide archive must be local"
            slide_path = (ROOT / unquote(slide_url.path)).resolve()
            assert slide_path.parent == (ROOT / "assets/files").resolve(), "Unexpected slide archive directory"
            assert slide_path.suffix.lower() == ".pdf" and slide_path.is_file(), "Missing slide archive: " + paper["id"]
            assert slide_path.read_bytes().startswith(b"%PDF-"), "Invalid slide PDF: " + paper["id"]
            local_slides.add(slide_path)
    page = Page()
    page.feed(markup)
    assert page.lang and page.title, "Missing language or page title"
    assert len(page.ids) == len(set(page.ids)), "Duplicate HTML ids"
    for reference in page.references:
        assert reference in page.ids, "Missing accessibility target: " + reference
    local_files = 0
    for url in page.links:
        parsed = urlsplit(url)
        assert parsed.scheme not in ("javascript", "data"), "Unexpected active link"
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path:
            path = ROOT / unquote(parsed.path.lstrip("/"))
            assert path.is_file(), "Missing local file: " + str(path)
            if path.suffix.lower() == ".pdf":
                assert path.resolve() in local_slides, "Only slide PDFs may be linked locally: " + url
            local_files += 1
        elif parsed.fragment:
            assert unquote(parsed.fragment) in page.ids, "Missing anchor: " + url
        else:
            raise AssertionError("Empty link")
    for stylesheet in (ROOT / "assets/css").glob("*.css"):
        for match in re.finditer(r"url\([\"']?([^\)\"']+)", stylesheet.read_text()):
            url = match.group(1)
            assert not urlsplit(url).scheme, "Unexpected externally hosted CSS asset: " + url
            assert (stylesheet.parent / url).is_file(), "Missing CSS asset: " + url
    local_pdfs = {path.resolve() for path in (ROOT / "assets").rglob("*.[pP][dD][fF]")}
    assert local_pdfs == local_slides, "Only declared slide archives may be stored as local PDFs"
    official_hosts = {"ieeexplore.ieee.org", "dl.acm.org", "link.springer.com", "link.springernature.com", "www.usenix.org", "arxiv.org"}
    for paper in publications:
        for resource in [{"url": paper["url"], "label": "Article"}] + paper.get("links", []):
            if resource["label"] in ("DOI", "Lightning talk"):
                continue
            if resource["label"] == "Slides" and resource["url"] == paper.get("local_slides"):
                continue
            assert urlsplit(resource["url"]).hostname in official_hosts, "Paper resource must use an official host: " + paper["id"]
    profile = json.loads((ROOT / "content/profile.json").read_text())
    for field in ("role", "company", "employer", "position", "employment", "work_experience"):
        assert not profile.get(field), "Employment field must not be published: " + field
    assert "software engineer" not in markup.lower(), "Old employment description remains"
    assert set(page.papers) == {paper["id"] for paper in publications}, "Publication lost or duplicated"
    papers_by_id = {paper["id"]: paper for paper in publications}
    for kind in ("preprint", "journal", "conference"):
        ordered = [papers_by_id[paper_id] for paper_id in page.papers if papers_by_id[paper_id]["type"] == kind]
        pinned_count = sum(bool(paper.get("pinned")) for paper in ordered)
        assert all(paper.get("pinned") for paper in ordered[:pinned_count]), "Pinned papers must lead their publication category"
        ordered = ordered[pinned_count:]
        coauthor_seen = False
        for paper in ordered:
            is_first_author = paper["authors"][0] == profile["name"]
            if not is_first_author:
                coauthor_seen = True
            else:
                assert not coauthor_seen, "First-author papers must lead each publication category"
        for first_author in (True, False):
            group = [p for p in ordered if (p["authors"][0] == profile["name"]) == first_author]
            dates = [p.get("publication_date", str(p["year"])) for p in group]
            dates = [value + "-01" * (2 - value.count("-")) for value in dates]
            assert all(newer >= older for newer, older in zip(dates, dates[1:])), "Publication chronology is incorrect"
    for paper in publications:
        if paper.get("award"):
            award = paper["award"]
            article = markup.split('<article id="' + paper["id"] + '"', 1)[1].split("</article>", 1)[0]
            honors = markup.split('<section id="awards"', 1)[1].split("</section>", 1)[0]
            assert award["label"] in unescape(article), "Award missing from publication"
            assert award["label"] in unescape(honors), "Award missing from honors"
            assert award["url"] in unescape(article) and award["url"] in unescape(honors), "Award source link missing"
    assert page.citations == len(publications), "Missing BibTeX entry"
    for placeholder in ("Your Name", "yourname", "Lorem ipsum", "UA-111540567-4", "teaser_example"):
        assert placeholder not in markup, "Template placeholder remains: " + placeholder
    if publications:
        bib = (ROOT / "assets/files/publications.bib").read_text()
        assert len(re.findall(r"^@(article|inproceedings|misc)\{", bib, re.M)) == len(publications), "Bibliography incomplete"
        for paper in publications:
            if paper["type"] == "preprint":
                assert "@misc{" + paper["id"] + "," in bib, "Preprint exported as a published paper"
                assert paper.get("eprint") and paper.get("archivePrefix"), "Preprint identifier missing"
                for field in ("eprint", "archivePrefix", "primaryClass"):
                    if paper.get(field):
                        assert "{} = {{{}}}".format(field, paper[field]) in bib, "Preprint metadata missing: " + field
    print("Passed: {} publications, {} citations, {} local asset links, unique anchors and accessible labels.".format(len(publications), page.citations, local_files))


if __name__ == "__main__":
    main()
