# Liedjes publiceren

## Dagelijks gebruik

Je werkt alleen in Google Drive.

```text
liedboek/
├── gepubliceerd/
└── concepten/
```

Een lied in `concepten` verschijnt niet op de site.

Verplaats een lied naar `gepubliceerd` zodra je het openbaar wilt maken.

De workflow draait automatisch bij een wijziging op `main` en daarnaast volgens het ingestelde schema. Je kunt hem ook handmatig starten via GitHub Actions.

## Documenttitel

De titel van het Google Doc wordt de titel van de webpagina.

Bijvoorbeeld:

`Where I Stop Running`

wordt:

`/liedjes/where-i-stop-running/`

## Metadata

Metadata is optioneel.

Zet dit blok helemaal bovenaan een Google Doc:

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

Het metadata-blok verschijnt niet op de website.

## Velden

- `tags`: kommagescheiden onderwerpen of trefwoorden
- `akkoorden`: `ja` of `nee`
- `buma`: `ja` of `nee`
- `jaar`: jaartal
- `taal`: bijvoorbeeld `nl`, `en`, `de` of `fr`
- `status`: bijvoorbeeld `concept`, `werkversie` of `definitief`

`onderwerpen:` blijft voorlopig ook werken als oudere naam voor `tags:`.

## Schrijfnotitie

Een lied kan één optionele schrijfnotitie krijgen. Zet die direct na het metadata-blok en vóór de eigenlijke liedtekst:

```text
[[schrijfnotitie]]
Vlak voor een optreden zei iemand: "Come on, let's kick some country ass."
In mijn hoofd werd dat meteen een lied.
[[/schrijfnotitie]]
```

De notitie mag uit meerdere regels of alinea's bestaan. Het blok zelf wordt niet als onderdeel van de songtekst getoond. Op de liedpagina verschijnt de inhoud onder **Schrijfnotitie**.

Laat het blok gewoon weg als er bij een lied niets te vertellen valt. Het is bedoeld voor oorsprong, aanleiding of een relevante vondst, niet als verplichte toelichting.

## Tags en Onderwerpen

Tags worden gebruikt om automatisch de pagina **Onderwerpen** én de pagina **Dwarsverbanden** op te bouwen.

Bijvoorbeeld:

```text
tags: onderweg, verlies, muziek
```

zorgt dat het lied onder de betreffende onderwerpen kan verschijnen. Op **Dwarsverbanden** worden verschillende tags samengebracht in bredere lijnen door het liedboek.

Je hoeft onderwerpen nergens vooraf aan te maken.

## Akkoorden

Bij:

```text
akkoorden: ja
```

verschijnt het lied ook op de pagina **Met akkoorden**. De website probeert bij zulke liedjes de positie van akkoorden en tekstregels intact te houden.

## BumaStemra

Gebruik:

```text
buma: ja
```

alleen als het betreffende werk daadwerkelijk bij BumaStemra is aangemeld.

## Jaar, taal en status

Deze velden worden als metadata bij het lied gebruikt.

Voorbeeld:

```text
jaar: 2026
taal: en
status: definitief
```

`status` is informatief. Een document in `gepubliceerd` wordt gepubliceerd, ongeacht de status.

Wil je een lied niet publiceren, zet het dan in `concepten`.

## Zonder metadata

Een Google Doc zonder metadata-blok wordt gewoon gepubliceerd en verschijnt in de alfabetische liedlijst.

## Publiceren

Een merge of push naar `main` start de website-build automatisch. Na alleen een wijziging in Google Drive kun je wachten op de geplande build of handmatig starten via:

**GitHub → Actions → Build liedboek → Run workflow**

In de log hoort bijvoorbeeld te staan:

```text
Gesynchroniseerd: 3 lied(en).
```
