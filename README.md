# RAWLS utils

## Description

Can read and flip horizontally a `.rawls` image.
Can read and convert `.rawls` generated synthesis image format into `.png`.

`.rawls` store all pixels values as *float* and keeps also information about generated image (renderer used).

`.rawls` contains 3 blocks and specific lines information within each block:
- IHDR: 
    - **First line:** next information line size into byte
    - **Second line:** `{width}` `{height}` `{nbChannels}`
- COMMENTS
    - **All lines:** information from the renderer as comment
- DATA
    - **First line:** data block size
    - **Next lines:** all pixels values as byte code at each line

## How it works ?

```
pip install -r requirements.txt
```

### Examples:

Convert all `.rawls` images of folder into `.png`: 
```
python utils/convert.py  --folder data/folder --output data/output
```


Merge all `.rawls` images of folder and save with step:
```
python utils/merge_step.py --folder data/folder --output data/output --step 10 --ext png
```

Flip all `.rawls` images of folder:
```
python utils/flip.py --folder data/folder --output data/output --flip h --ext png
```