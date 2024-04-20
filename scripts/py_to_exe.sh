#!/bin/bash

# Generate exec file
source g://Anaconda3/etc/profile.d/conda.sh
conda activate py38
pyinstaller --onefile ../scripts/player.py

# Clean up folders
mv dist/player.exe player.exe
rm -r build
rm -r dist
rm player.spec
