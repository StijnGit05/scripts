# wanted folder

Scripts for creating wanted-poster PDFs from images.

- `make_posters.py`: Paste photos onto a poster template and save results to `OUTPUT_FOLDER`. Configure template and folder constants at the top of the file.
- `make_PDF.py`: Combine images from a folder into a single PDF. Configure `folder_path` and `output_pdf_path` inside the script or update to read from a config file.

Requirements: `Pillow`, `fpdf`.

Usage examples:

```bash
python "make_posters.py"
python "make_PDF.py"
```

Note: Paths in these scripts are currently hard-coded; consider updating them to use config files or command-line arguments for portability.
