# Skill: Cell Segmentation with Cellpose

## Context

This skill runs cell segmentation on fluorescence microscopy images using Cellpose. Use this when you have images of cells (phase contrast, DAPI, or membrane stain) and need to generate segmentation masks and extract per-cell measurements.

## Inputs

- **Image directory**: Path to directory containing .tif images
- **Channel configuration**: Which channel contains nuclei, which contains cytoplasm (if applicable)
- **Model**: Cellpose model to use (default: `cyto3` for whole-cell, `nuclei` for nuclear-only)
- **Diameter**: Expected cell diameter in pixels (or `None` for auto-detection)
- **Output directory**: Where to save masks and measurements

## Procedure

### Step 1 — Scan and validate images

1. List all .tif files in the image directory
2. Read the first image to determine dimensions, number of channels, bit depth
3. Report: number of images, dimensions, channels detected
4. If images are multi-channel, confirm channel assignment with user

**Stop and ask if:** no .tif files found, images have unexpected dimensions, channel assignment is unclear.

### Step 2 — Run segmentation

1. Initialize Cellpose model with specified model type
2. For each image:
   a. Load image
   b. Run segmentation with specified parameters
   c. Save mask as `{original_name}_mask.tif` in output directory
3. Report progress every 10 images

### Step 3 — Quality control

1. For each mask, compute:
   - Number of detected cells
   - Mean and median cell area (in pixels)
   - Fraction of image area covered by cells
2. Flag images where:
   - Zero cells detected
   - Mean cell area is >3 SD from the batch mean
   - Cell count is >3 SD from the batch mean
3. Save QC summary to `{output_dir}/segmentation_qc.csv`
4. Generate a QC montage: 3×3 grid showing representative images with mask overlays

### Step 4 — Extract measurements

For each cell in each image, measure:
- Cell area (pixels and µm² if pixel size is available)
- Centroid coordinates (x, y)
- Mean intensity in each channel
- Integrated intensity in each channel
- Eccentricity (shape measure)

Save to `{output_dir}/cell_measurements.csv` with columns: `image_id, cell_id, area_px, centroid_x, centroid_y, mean_intensity_ch1, ...`

### Step 5 — Summary

Report:
- Total images processed
- Total cells segmented
- Mean ± SD cells per image
- Any QC flags raised
- Output file locations

## Failure modes

| Issue | What to do |
|-------|-----------|
| Image can't be read | Skip, log the error, continue with remaining images |
| Cellpose GPU not available | Fall back to CPU, warn about slower processing |
| Zero cells in an image | Log as QC flag, include in report |
| Out of memory | Reduce batch size, process images one at a time |

## Dependencies

```python
from cellpose import models
import numpy as np
from skimage import io, measure
import pandas as pd
```
