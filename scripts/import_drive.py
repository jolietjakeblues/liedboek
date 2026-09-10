#!/usr/bin/env python3
import html
import io
import json
import os
import re
import unicodedata
from pathlib import Path

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SONGS = DOCS / "liedjes"
TOPICS = DOCS / "onderwerpen"
DATA = DOCS / "_data"
GOOGLE_DOC_MIME = "application/vnd.google-apps.document"

META_RE = re.compile(
    r"^\s*\[\[liedboek\]\]\s*\n(.*?)\n\s*\[\[/liedboek\]\]\s*\n?",
    re.I | re.S,
)

STATUS_LABELS = {
    "concept": "Concept",
    "werkversie": "Werkversie",
    "definitief": "Definitief",
}

LANGUAGE_LABELS = {
    "nl": "Nederlands",
    "en": "Engels",
    "de": "Duits",
    "fr": "Frans",
}


def slugify(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "lied"


def first_letter(value):
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").strip()
    if not ascii_value:
        return "#"
    char = ascii_value[0].upper()
    return char if "A" <= char <= "Z" else "#"


def yes(value):
    return str(value).strip().lower() in {"ja", "yes", "true", "1", "y"}


def parse_tags(value):
    return [x.strip() for x in value.split(",") if x.strip()]


def parse_metadata(text):
    meta = {
        "tags": [],
        "akkoorden": False,
        "buma": False,
        "jaar": "",
        "taal": "",
        "status": "",
    }

    match = META_RE.match(text)
    if not match:
        return meta, text.strip()

    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if key in {"tags", "onderwerpen"}:
            meta["tags"] = parse_tags(value)
        elif key == "akkoorden":
            meta["akkoorden"] = yes(value)
        elif key == "buma":
            meta["buma"] = yes(value)
        elif key == "jaar":
            meta["jaar"] = value
        elif key == "taal":
            meta["taal"] = value.lower()
        elif key == "status":
            meta["status"] = value.lower()

    return meta, text[match.end():].strip()


def service():
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=credentials, cache_discovery=False)


def list_docs(api, folder_id):
    q = (
        f"'{folder_id}' in parents and "
        f"mimeType='{GOOGLE_DOC_MIME}' and trashed=false"
    )
    out = []
    token = None

    while True:
        response = api.files().list(
            q=q,
            spaces="drive",
            fields="nextPageToken, files(id,name,modifiedTime)",
            orderBy="name_natural",
            pageToken=token,
        ).execute()
        out += response.get("files", [])
        token = response.get("nextPageToken")
        if not token:
            return out


def export_text(api, file_id):
    request = api.files().export_media(fileId=file_id, mimeType="text/plain")
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return (
        buffer.getvalue()
        .decode("utf-8-sig")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def fm(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def topic_link(tag):
    return (
        f'<a href="{{{{ site.baseurl }}}}/onderwerpen/{slugify(tag)}/">'
        f"{html.escape(tag)}</a>"
    )


def song_page(item):
    tags_html = ""
    if item["tags"]:
        links = " · ".join(topic_link(tag) for tag in item["tags"])
        tags_html = f'<p class="meta">Onderwerpen: {links}</p>'

    year_html = (
        f'<p class="meta">Jaar: {html.escape(item["jaar"])}</p>'
        if item["jaar"] else ""
    )

    language_html = ""
    if item["taal"]:
        language = LANGUAGE_LABELS.get(item["taal"], item["taal"])
        language_html = f'<p class="meta">Taal: {html.escape(language)}</p>'

    status_html = ""
    if item["status"]:
        status = STATUS_LABELS.get(item["status"], item["status"])
        status_html = f'<p class="meta">Status: {html.escape(status)}</p>'

    buma_html = (
        '<p class="meta">Dit werk is aangemeld bij BumaStemra.</p>'
        if item["buma"] else ""
    )

    lyrics_class = "lyrics has-chords" if item["akkoorden"] else "lyrics"

    return (
        "---\n"
        "layout: song\n"
        f'title: "{fm(item["title"])}"\n'
        f'permalink: /liedjes/{item["slug"]}/\n'
        "---\n\n"
        f'<pre class="{lyrics_class}">{html.escape(item["text"])}</pre>\n\n'
        f"{tags_html}\n"
        f"{year_html}\n"
        f"{language_html}\n"
        f"{status_html}\n"
        '<p class="rights">© Joop Vanderheiden. Alle rechten voorbehouden.</p>\n'
        f"{buma_html}\n"
    )


def compact_meta(item):
    parts = []
    if item["taal"]:
        parts.append(LANGUAGE_LABELS.get(item["taal"], item["taal"]))
    if item["jaar"]:
        parts.append(html.escape(item["jaar"]))
    if item["akkoorden"]:
        parts.append("met akkoorden")
    return parts


def write_index(items):
    ordered = sorted(items, key=lambda x: x["title"].casefold())
    groups = {}
    for item in ordered:
        groups.setdefault(first_letter(item["title"]), []).append(item)

    lines = [
        "---",
        "layout: default",
        'title: "Liedjes"',
        "permalink: /liedjes/",
        "---",
        "",
        "# Liedjes",
        "",
        '<div class="song-tools">',
        '<input id="song-search" class="search" type="search" placeholder="Zoek een lied..." aria-label="Zoek een lied">',
        '<div class="song-filters" role="group" aria-label="Filter liedjes">',
        '<button type="button" class="filter is-active" data-filter="all">Alle</button>',
        '<button type="button" class="filter" data-filter="nl">Nederlands</button>',
        '<button type="button" class="filter" data-filter="en">Engels</button>',
        '<button type="button" class="filter" data-filter="chords">Met akkoorden</button>',
        "</div>",
        "</div>",
        "",
        '<nav class="alphabet" aria-label="Alfabet">',
    ]

    for letter in groups:
        lines.append(f'<a href="#letter-{letter.lower()}">{letter}</a>')
    lines += ["</nav>", "", '<div id="song-list" class="song-groups">']

    for letter, group in groups.items():
        lines += [
            f'<section class="song-group" data-letter="{letter}">',
            f'<h2 id="letter-{letter.lower()}" class="letter-heading">{letter}</h2>',
            '<ul class="song-list">',
        ]
        for item in group:
            title = html.escape(item["title"])
            folded = html.escape(item["title"].casefold(), quote=True)
            tags_search = html.escape(" ".join(item["tags"]).casefold(), quote=True)
            language = html.escape(item["taal"], quote=True)
            chords = "true" if item["akkoorden"] else "false"

            meta_parts = compact_meta(item)
            meta_bits = [html.escape(part) for part in meta_parts]
            if item["tags"]:
                meta_bits.extend(topic_link(tag) for tag in item["tags"][:3])

            lines += [
                (
                    f'<li class="song-list-item" data-title="{folded}" '
                    f'data-tags="{tags_search}" data-language="{language}" '
                    f'data-chords="{chords}">'
                ),
                f'<a class="song-title" href="{{{{ site.baseurl }}}}/liedjes/{item["slug"]}/">{title}</a>',
            ]
            if meta_bits:
                lines.append(
                    '<div class="song-summary">' + " · ".join(meta_bits) + "</div>"
                )
            lines.append("</li>")
        lines += ["</ul>", "</section>"]

    lines += [
        "</div>",
        '<p id="song-empty" class="song-empty" hidden>Geen liedjes gevonden.</p>',
        "",
        '<script src="{{ site.baseurl }}/assets/search.js"></script>',
        "",
    ]
    (SONGS / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_chords(items):
    selected = [x for x in items if x["akkoorden"]]
    lines = [
        "---",
        "layout: default",
        'title: "Met akkoorden"',
        "permalink: /akkoorden/",
        "---",
        "",
        "# Met akkoorden",
        "",
    ]
    if selected:
        for item in sorted(selected, key=lambda x: x["title"].casefold()):
            lines.append(
                f'- [{item["title"]}]({{{{ site.baseurl }}}}/liedjes/{item["slug"]}/)'
            )
    else:
        lines.append("Nog geen liedjes gemarkeerd als lied met akkoorden.")
    lines.append("")
    (DOCS / "akkoorden.md").write_text("\n".join(lines), encoding="utf-8")


def write_topics(items):
    TOPICS.mkdir(parents=True, exist_ok=True)
    for path in TOPICS.glob("*.md"):
        path.unlink()

    by_topic = {}
    for item in items:
        for tag in item["tags"]:
            by_topic.setdefault(tag, []).append(item)

    overview = [
        "---",
        "layout: default",
        'title: "Onderwerpen"',
        "permalink: /onderwerpen/",
        "---",
        "",
        "# Onderwerpen",
        "",
    ]

    if not by_topic:
        overview.append("Nog geen onderwerpen toegevoegd.")
    else:
        for topic in sorted(by_topic, key=str.casefold):
            slug = slugify(topic)
            overview.append(
                f'- [{topic}]({{{{ site.baseurl }}}}/onderwerpen/{slug}/)'
            )
            page = [
                "---",
                "layout: default",
                f'title: "{fm(topic)}"',
                f"permalink: /onderwerpen/{slug}/",
                "---",
                "",
                f"# {topic}",
                "",
            ]
            for item in sorted(by_topic[topic], key=lambda x: x["title"].casefold()):
                page.append(
                    f'- [{item["title"]}]({{{{ site.baseurl }}}}/liedjes/{item["slug"]}/)'
                )
            page.append("")
            (TOPICS / f"{slug}.md").write_text("\n".join(page), encoding="utf-8")

    (DOCS / "onderwerpen.md").write_text(
        "\n".join(overview) + "\n",
        encoding="utf-8",
    )


def main():
    folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]
    SONGS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    for path in SONGS.glob("*.md"):
        if path.name != "index.md":
            path.unlink()

    api = service()
    docs = list_docs(api, folder_id)

    items = []
    used_slugs = set()

    for doc in docs:
        title = doc["name"].strip()
        slug = slugify(title)
        if slug in used_slugs:
            slug = f"{slug}-{doc['id'][:6].lower()}"
        used_slugs.add(slug)

        meta, body = parse_metadata(export_text(api, doc["id"]))
        item = {"title": title, "slug": slug, "text": body, **meta}
        items.append(item)

        (SONGS / f"{slug}.md").write_text(song_page(item), encoding="utf-8")

    write_index(items)
    write_chords(items)
    write_topics(items)

    public_search = [
        {
            "title": x["title"],
            "url": f"/liedjes/{x['slug']}/",
            "tags": x["tags"],
            "taal": x["taal"],
            "status": x["status"],
            "jaar": x["jaar"],
            "akkoorden": x["akkoorden"],
        }
        for x in items
    ]
    (DATA / "songs.json").write_text(
        json.dumps(public_search, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Gesynchroniseerd: {len(items)} lied(en).")


if __name__ == "__main__":
    main()
