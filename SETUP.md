# Eenmalige installatie

Deze documentatie beschrijft de huidige inrichting van het liedboek.

## 1. GitHub

Repository:

`jolietjakeblues/liedboek`

De website wordt gebouwd met GitHub Actions en gepubliceerd met GitHub Pages.

De repository mag openbaar zijn. De liedteksten zelf worden niet naar GitHub gecommit. Ze bestaan alleen tijdelijk tijdens de build en in de uiteindelijke openbare website.

## 2. Google Drive

Gebruik deze structuur:

```text
liedboek/
├── gepubliceerd/
└── concepten/
```

Alleen Google Docs die rechtstreeks in `gepubliceerd` staan, worden gepubliceerd.

De map `concepten` wordt niet gedeeld met de automatisering.

## 3. Google Cloud

Voor de koppeling met GitHub Actions wordt Google Workload Identity Federation gebruikt.

Benodigd:

- Google Drive API ingeschakeld
- service-account voor het liedboek
- Workload Identity Pool
- OIDC-provider voor GitHub Actions
- IAM-koppeling waarmee alleen deze repository het service-account mag gebruiken

Huidige service-account:

`liedboek-sync@project-45e94b35-46b4-4c56-98a.iam.gserviceaccount.com`

GitHub Actions gebruikt dus geen gedownloade JSON-key.

## 4. Deel alleen de publicatiemap

Open in Google Drive:

`liedboek/gepubliceerd`

Deel alleen deze map met:

`liedboek-sync@project-45e94b35-46b4-4c56-98a.iam.gserviceaccount.com`

Rol:

`Viewer`

De map `concepten` hoeft niet te worden gedeeld.

## 5. Google Drive map-ID

Open `liedboek/gepubliceerd`.

Een URL ziet er bijvoorbeeld zo uit:

`https://drive.google.com/drive/folders/1AbCdEfGh...`

Het gedeelte na `/folders/` is het map-ID.

Voor deze installatie is het map-ID van `gepubliceerd`:

`1g6TCtspMICAHz-_DeW-zwH3hvAaoB27_`

## 6. GitHub secret

Ga naar:

**Settings → Secrets and variables → Actions**

Maak één repository secret:

### `GOOGLE_DRIVE_FOLDER_ID`

Waarde:

`1g6TCtspMICAHz-_DeW-zwH3hvAaoB27_`

Er is geen `GOOGLE_SERVICE_ACCOUNT_JSON` nodig.

## 7. GitHub Pages

Ga naar:

**Settings → Pages**

Kies:

**Build and deployment → Source → GitHub Actions**

## 8. Workflow

De workflow staat in:

`.github/workflows/build-liedboek.yml`

Hij doet achtereenvolgens:

1. repository ophalen
2. Python installeren
3. Drive-afhankelijkheden installeren
4. via OIDC authenticeren bij Google Cloud
5. Google Docs uit `gepubliceerd` lezen
6. tijdelijke Markdown genereren
7. de site met Jekyll bouwen
8. het GitHub Pages-artifact publiceren

De workflow draait automatisch volgens het ingestelde schema en kan ook handmatig worden gestart via:

**Actions → Build liedboek → Run workflow**

## 9. Beveiliging

Aanbevolen repositorybeveiliging:

- bescherm `main`
- blokkeer force pushes
- blokkeer verwijderen van `main`
- werk via pull requests
- laat vereiste statuschecks slagen voor merge
- gebruik Dependabot voor Python en GitHub Actions

Voor Google geldt:

- geen statische JSON-key
- alleen OIDC / Workload Identity Federation
- alleen de map `gepubliceerd` delen
- service-account alleen leesrechten geven

## 10. Zoekmachines

De site gebruikt standaard `noindex, noarchive` en een `robots.txt` die crawlers vraagt niet te indexeren.

Dat vermindert vindbaarheid en caching, maar is geen kopieerbeveiliging. Openbaar leesbare tekst kan technisch altijd worden gekopieerd.
