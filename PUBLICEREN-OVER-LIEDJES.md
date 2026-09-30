# Over liedjes publiceren

De nieuwe rubriek **Over liedjes** leest automatisch Google Docs uit de Drive-map:

```text
overliedjes/
```

De map moet gedeeld zijn met dezelfde service-account als `gepubliceerd`:

`liedboek-sync@project-45e94b35-46b4-4c56-98a.iam.gserviceaccount.com`

Viewer is voldoende.

## Documentnaam

De eenvoudigste vorm:

```text
Hier gehör ich hin — Johannes Oerding
```

De importer splitst dat automatisch in titel en artiest.

## Optionele metadata

Wil je ook een korte intro op de overzichtspagina, zet dan bovenaan:

```text
[[overliedjes]]
titel: Hier gehör ich hin
artiest: Johannes Oerding
intro: Over thuiskomen, identiteit en de kracht van een eenvoudige regel.
[[/overliedjes]]
```

Daarna volgt gewoon het artikel.

De stukken komen automatisch onder:

```text
/over-liedjes/
```

en krijgen elk hun eigen pagina.
