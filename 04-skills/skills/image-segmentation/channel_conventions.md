# Channel Conventions

Standard channel ordering by stain panel used in this lab.

## Immunofluorescence (3-channel)

| Channel | Stain     | Purpose         |
|---------|-----------|-----------------|
| 1       | DAPI      | Nuclei          |
| 2       | CellMask  | Cytoplasm/membrane |
| 3       | Target Ab | Protein of interest |

## Live imaging (2-channel)

| Channel | Stain        | Purpose   |
|---------|--------------|-----------|
| 1       | Hoechst      | Nuclei    |
| 2       | Calcein-AM   | Viability |

## Cellpose channel mapping

Cellpose expects `channels = [cytoplasm_channel, nucleus_channel]`:
- If you have cytoplasm + nucleus: `channels = [2, 1]`
- If nucleus only: `channels = [0, 0]` (grayscale)
- If cytoplasm only: `channels = [1, 0]`

Channel numbers are **1-indexed** in Cellpose (0 means not present).
