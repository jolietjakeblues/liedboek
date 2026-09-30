# Fix: Over liedjes

Deze versie herstelt drie dingen tegelijk:

- `overliedjes` leest nu zowel **Google Docs als `.md`-bestanden** uit Drive.
- Markdown wordt verder **ongewijzigd** aan Jekyll/Kramdown doorgegeven. Gewone HTML, dus ook een Spotify `<iframe>`, werkt rechtstreeks in het `.md`-bestand.
- `[[spotify]] ... [[/spotify]]` blijft werken voor bestaande teksten, maar is niet nodig.
- De desktop-header is verbreed zodat `Over` niet alleen op een tweede regel valt.

Vervang:

- `scripts/import_drive.py`
- `docs/assets/style.css`

Daarna merge naar `main`. De bestaande push-trigger bouwt de site automatisch opnieuw.
