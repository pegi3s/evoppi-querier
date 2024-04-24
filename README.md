<img src="https://github.com/pegi3s/evoppi-querier/raw/master/resources/evoppi.png" align="right" />

# EvoPPI Querier [![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/pegi3s/evoppi-querier) [![dockerhub](https://img.shields.io/badge/hub-docker-blue)](https://hub.docker.com/r/pegi3s/evoppi-querier)

The `pegi3s/evoppi-querier` Docker image allows making queries to the [EvoPPI web server](http://evoppi.i3s.up.pt/).

# Single species

The main script is `query_single_species`, so you should adapt and run the following command:
```sh
docker run --rm -v /your/data/dir:/data -w /data pegi3s/evoppi-querier query_single_species -c config.txt -o output_dir
```

In this command, you should replace:
- `/your/data/dir` to point to the directory that contains the file you want to process.
- `config.txt` to the actual name of your input TXT file with the configuration parameters (see below).
- `output_dir` to the actual name of your output directory.

The script help can be obtained with `docker run --rm pegi3s/evoppi-querier query_single_species --help`.

## Configuration parameters

These are the configuration parameters that must be included in the configuration text file:

```
Species=Homo sapiens
GeneID=411
Int_level=1
Format=single
Interactome.Databases=BioGRID; HIPPIE
Interactome.Modifiers_22=Homo sapiens (Modifiers_22)
Interactome.polyQ_22=Homo sapiens (PolyQ_22)
Predictome.Databases=Based on Drosophila melanogaster BioGRID (DIOPT); Based on Drosophila melanogaster BioGRID (ENSEMBL)
Predictome.Modifiers_22=
Predictome.polyQ_22=Homo sapiens Danio rerio (from DIOPT) (PolyQ_models_22)
```

Note that:
- The names of the `Species` supported can be obtained with the following command: `docker run --rm pegi3s/evoppi-querier list_species`.
- The names of the interactomes for the `Interactome.*` parameters can be obtained with the following command: `docker run --rm pegi3s/evoppi-querier list_interactomes --species <Species> -dt interactome`.
- The names of the predictomes for the `Predictome.*` parameters can be obtained with the following command: `docker run --rm pegi3s/evoppi-querier list_interactomes --species <Species> -dt predictome`.
- All parameters are mandatory, otherwise the program will not run. `Interactome.*` and `Predictome.*` may be empty and at least one itneractome/predictome name must be provided.

## Test data

To test the `query_single_species` script, start creating a new file named `config.txt` with the previous example configuration. And then run the following command:

```sh
docker run --rm -v "$(pwd):$(pwd)" -w "$(pwd)" pegi3s/evoppi-querier query_single_species -c config.txt -o output_dir
```

The result will be available in the new `output_dir` directory created at your current working directory. As `Format=single`, this directory will contain a single file named `EvoPPI_Results.csv`.

# Changelog

The `latest` tag contains always the most recent version.

## [1.0.1] - 24/01/2024

- Fixes a bug when retrieving query results that caused the first ten interactions were missing.

## [1.0.0] - 22/01/2024

- Initial `pegi3s/evoppi-querier` version containing the `query_single_species` script.