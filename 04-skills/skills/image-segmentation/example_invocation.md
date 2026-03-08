# Example: Running the Cell Segmentation Skill

## Prompt

```
Run cell segmentation on the images in data/raw/experiment_2025-03-01/:
- Use the cyto3 model
- Nuclei are in channel 1 (DAPI), cytoplasm in channel 2 (CellMask)
- Expected cell diameter: 60 pixels
- Save results to results/segmentation/
```

## What Claude does

1. Reads the skill file for the full procedure
2. Scans the image directory, reports what it finds
3. Runs Cellpose on each image, saves masks
4. Runs QC checks, flags any problems
5. Extracts per-cell measurements
6. Generates QC montage and summary
