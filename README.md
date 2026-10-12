# Change Bunch Of Files

This repository is now organized into folders by purpose.

## Structure

- `gpx/`
  - `GPXgetHight.py`
  - `GPXThing.py`
  - `example.configGPX.json`
  - `configGPX.json` (local config file, ignored by git)
- `photo/`
  - `MetaDataFotoChange.py`
  - `example.configFoto.json`
  - `configFoto.json` (local config file, ignored by git)
- `misc/`
  - `invert.py`
  - `SplitPDF.py`
  - `example.configInvert.json`
  - `example.configSplitPDF.json`
  - `configInvert.json` (local config file, ignored by git)
  - `configSplitPDF.json` (local config file, ignored by git)
- `wanted folder/`
  - `make_PDF.py`
  - `make_posters.py`
  - `readme`

## Config usage

Each script loads its config from the same folder as the script. Copy the example config file to the local config file name and update it before running:

- `gpx/example.configGPX.json` -> `gpx/configGPX.json`
- `photo/example.configFoto.json` -> `photo/configFoto.json`

The local config files are ignored by git, so they can safely contain your personal input/output paths.

## Run

- `python gpx/GPXgetHight.py`
- `python photo/MetaDataFotoChange.py`

