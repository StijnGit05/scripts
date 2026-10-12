# photo

Photo metadata utilities.

- `MetaDataFotoChange.py`: Update EXIF date and GPS tags for JPG/JPEG images. Configure `configFoto.json` (example included) and run. The script uses `piexif` and `Pillow` to read/write EXIF data.

Requirements: `Pillow`, `piexif`.

Usage:

```bash
python MetaDataFotoChange.py
```

Back up your photos before running the script; EXIF updates are destructive.
