# Liedboek

Persoonlijk liedboek met Google Drive als bron en GitHub Pages als publicatieplek.

## Hoe het werkt

```text
Google Drive
  liedboek/
  ├── gepubliceerd/
  └── concepten/
        ↓
GitHub Actions
        ↓
tijdelijke Markdown-bestanden
        ↓
Jekyll
        ↓
GitHub Pages
```

Google Drive is de bron. Liedteksten worden niet naar GitHub gecommit.

De GitHub Action leest alleen documenten uit de gedeelde map `gepubliceerd`, maakt tijdens de build tijdelijke Markdown-bestanden en publiceert alleen het gebouwde GitHub Pages-resultaat.

Documenten in `concepten` worden niet gepubliceerd.

## Website

De site staat op:

`https://jolietjakeblues.github.io/liedboek/`

De site bevat onder meer:

- een alfabetische liedlijst
- onderwerpen op basis van tags
- een overzicht van liedjes met akkoorden
- per lied optionele metadata zoals jaar, taal, status en BumaStemra-vermelding

## Metadata in Google Docs

Metadata is optioneel. Zet het blok helemaal bovenaan een Google Doc:

```text
[[liedboek]]
tags: onderweg, identiteit, volhouden
akkoorden: nee
buma: nee
jaar: 2026
taal: en
status: definitief
[[/liedboek]]
```

`onderwerpen:` blijft voorlopig ook ondersteund als oudere naam voor `tags:`.

Zie `PUBLICEREN.md` voor dagelijks gebruik.

## Techniek en beveiliging

- Google Drive is de bron.
- Alleen `gepubliceerd` wordt gedeeld met het service-account.
- GitHub Actions gebruikt Google Workload Identity Federation / OIDC.
- Het enige vereiste repository secret is `GOOGLE_DRIVE_FOLDER_ID`.
- Liedteksten worden niet als bronbestanden in de GitHub-repository opgeslagen.
- De site vraagt zoekmachines standaard om niet te indexeren of cachen.
- Er staat bewust geen open-sourcelicentie op de liedteksten.

Zie `SETUP.md` voor de technische inrichting.

Copyright © Joop Vanderheiden. Alle rechten voorbehouden.
