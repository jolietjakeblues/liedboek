# Installeren

Deze update bouwt drie afgesproken functies:

1. **Dwarsverbanden** op basis van bestaande tags.
2. **Schrijfnotities** als optioneel blok per Google Doc.
3. Een **push-trigger op `main`**, zodat een merge meteen een nieuwe Pages-build start.

## Bestanden vervangen

Kopieer deze bestanden naar dezelfde paden in de repository:

- `.github/workflows/build-liedboek.yml`
- `scripts/import_drive.py`
- `docs/_layouts/default.html`
- `docs/index.md`
- `docs/assets/style.css`
- `docs/dwarsverbanden.md`
- `PUBLICEREN.md`

Werk bij voorkeur in een nieuwe branch en maak daarna een pull request naar `main`.

## Test na de merge

De merge naar `main` hoort nu vanzelf **Build liedboek** te starten.

Controleer daarna:

- `/dwarsverbanden/`
- een lied zonder schrijfnotitie
- een lied mét schrijfnotitie
- de bestaande pagina `/liedjes/`
- een lied met akkoorden

## Voorbeeld schrijfnotitie

Direct na `[[/liedboek]]` en vóór de tekst:

```text
[[schrijfnotitie]]
Vlak voor een optreden zei iemand: "Come on, let's kick some country ass."
In mijn hoofd werd dat meteen een lied.
[[/schrijfnotitie]]
```

Het blok is optioneel.

## Opmerking

De ChatGPT-GitHub-koppeling kan de repository wel lezen, maar weigert op dit moment het aanmaken van branches met HTTP 403. Daarom is deze update als compleet pakket gemaakt in plaats van rechtstreeks als PR.
