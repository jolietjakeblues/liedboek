# Eenmalige installatie

## 1. GitHub

Repository:

`jolietjakeblues/liedboek`

Plaats de inhoud van dit pakket in de root van de repository en commit naar `main`.

De repository mag openbaar blijven. De liedteksten zelf worden niet naar GitHub gecommit. Ze bestaan alleen tijdelijk tijdens de GitHub Actions-build en in de uiteindelijke openbare website.

## 2. Drive-structuur

Maak in Google Drive:

```text
liedboek/
├── gepubliceerd/
│   ├── Where I Stop Running
│   └── ...
└── concepten/
    └── ...
```

Verplaats alleen liedjes die openbaar mogen zijn naar `gepubliceerd`.

De GitHub Action krijgt uitsluitend toegang tot de map `gepubliceerd`.

## 3. Google Cloud

1. Open Google Cloud Console.
2. Maak een project, bijvoorbeeld `liedboek`.
3. Schakel de Google Drive API in.
4. Maak een Service Account.
5. Maak een JSON-key voor dat Service Account.
6. Bewaar die JSON-key veilig.

## 4. Deel alleen de publicatiemap

Open in Drive de map:

`liedboek/gepubliceerd`

Deel alleen deze map met het e-mailadres van het Service Account.

Viewer is voldoende.

De map `concepten` hoef je niet te delen.

## 5. Google Drive map-ID

Open `liedboek/gepubliceerd`.

De URL lijkt op:

`https://drive.google.com/drive/folders/1AbCdEfGh...`

Het gedeelte na `/folders/` is het map-ID.

## 6. GitHub Secrets

Ga naar:

**Settings → Secrets and variables → Actions**

Maak:

### `GOOGLE_DRIVE_FOLDER_ID`

Het ID van de map `gepubliceerd`.

### `GOOGLE_SERVICE_ACCOUNT_JSON`

Plak de volledige inhoud van de JSON-key.

Zet de JSON-key zelf nooit in GitHub.

## 7. GitHub Pages

Ga naar:

**Settings → Pages**

Kies:

**Build and deployment → Source → GitHub Actions**

## 8. Eerste publicatie

Ga naar:

**Actions → Build liedboek → Run workflow**

Daarna hoort de site beschikbaar te zijn op:

`https://jolietjakeblues.github.io/liedboek/`

## 9. Zoekmachines

De site gebruikt standaard `noindex, noarchive` en een `robots.txt` die crawlers tegenhoudt.

Dit verkleint vindbaarheid en caching, maar maakt kopiëren niet onmogelijk.
