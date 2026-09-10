# Installatie van deze update

Deze map bevat alleen de bestanden die gewijzigd of toegevoegd moeten worden.

Vervang in de repository:

- `scripts/import_drive.py`
- `docs/assets/search.js`
- `docs/assets/style.css`
- `docs/404.html`

`METADATA-VOORSTELLEN.md` is een werkdocument voor het handmatig bijwerken van de Google Docs en hoeft niet per se in de repository.

Na merge naar `main`:

1. start `Build liedboek` handmatig
2. controleer dat `Gesynchroniseerd: N lied(en).` in de log staat
3. test `/liedjes/`
4. test een lied met akkoorden op desktop en mobiel
5. test een niet-bestaande URL voor de nieuwe 404

De GitHub-koppeling van ChatGPT kan momenteel geen branch aanmaken of bestanden schrijven (403), dus deze update kon niet rechtstreeks als PR worden geplaatst.
