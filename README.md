# CoreSignal

CoreSignal is a reproducible computational research framework for testing whether independently inferred inner-core dynamics have predictive power for Earth-rotation and geomagnetic observations.

## Research question

Can time-varying inner-core differential rotation and deformation be quantitatively connected to measurable variations in Earth's length of day (LOD) and geomagnetic secular variation?

## Character policy

All repository-controlled source code, documentation, notebooks, manuscript source, configuration, metadata, and text-bearing figure assets must use English and standard scientific notation.

CI rejects Chinese, Japanese, Korean, CJK punctuation, fullwidth CJK forms, and the CJK Unicode blocks defined in `scripts/check_english_only.py`.

The scanner covers source code, documentation, notebooks, manuscript files, vector figures, and decodable figure metadata. Raster pixels are not OCR-scanned by CI; authoritative figure labels must also exist in text or vector source.

Run locally:

```bash
python scripts/check_english_only.py .
python -m unittest discover -s tests -v
```
