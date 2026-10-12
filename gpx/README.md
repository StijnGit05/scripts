# gpx

This folder contains GPX-related utilities.

- `GPXThing.py`: Interpolates points along GPX tracks to a fixed interval (default 10 meters). Usage: configure `INPUT_GPX_FILE`, `OUTPUT_GPX_FILE` or call `process_gpx(input, output, interval)`. The script is safe to import (has a `if __name__ == "__main__"` entry).
- `GPXgetHight.py`: Fetches elevation data for GPX points (uses OpenTopoData/test-dataset in the example). Configure `configGPX.json` (example included) and run the script to produce an updated GPX with elevation tags.
- `example.configGPX.json`: Example config file used by `GPXgetHight.py`.

Requirements: `gpxpy`, `requests` (also listed in top-level `requirements.txt`).

Usage examples:

```bash
python GPXThing.py
python GPXgetHight.py
```

Adjust config files and script constants before running.
