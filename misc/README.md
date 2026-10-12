# misc

Utilities for simple file processing tasks.

- `invert.py`: Inverts image colors. Configure `configInvert.json` (example included) with `INPUT_IMAGE` and `OUTPUT_IMAGE`, then run.
- `SplitPDF.py`: Splits a PDF into one-file-per-page. Configure `configSplitPDF.json` (example included) with `PDF_PATH`, then run.

Requirements: `Pillow`, `PyPDF2`.

Usage examples:

```bash
python invert.py
python SplitPDF.py
```

Files are safe to import; they include `if __name__ == "__main__"` guards.
