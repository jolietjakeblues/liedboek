# Liedjes publiceren

## Normaal gebruik

Je werkt alleen in Google Drive.

```text
liedboek/
├── gepubliceerd/
└── concepten/
```

Een lied in `concepten` verschijnt niet op de site.

Verplaats een lied naar `gepubliceerd` zodra je het openbaar wilt maken.

De workflow draait automatisch iedere 6 uur. Je kunt hem ook handmatig starten via GitHub Actions.

## Documenttitel

De titel van het Google Doc wordt de titel van de webpagina.

Bijvoorbeeld:

`Where I Stop Running`

wordt:

`/liedjes/where-i-stop-running/`

## Optionele metadata

Je hoeft geen metadata toe te voegen.

Als je later onderwerpen, akkoorden of Buma-status wilt vastleggen, kun je helemaal bovenaan het Google Doc dit blok gebruiken:

```text
[[liedboek]]
onderwerpen: afscheid, onderweg
akkoorden: ja
buma: ja
jaar: 2026
[[/liedboek]]

Hier begint de eigenlijke liedtekst...
```

Het blok verschijnt niet op de website.

Ondersteunde velden:

- `onderwerpen`: kommagescheiden trefwoorden
- `akkoorden`: `ja` of `nee`
- `buma`: `ja` of `nee`
- `jaar`: jaartal

Zonder metadata komt het lied gewoon in de alfabetische lijst.
