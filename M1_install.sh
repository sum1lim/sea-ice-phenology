#!/bin/bash

curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh" --output ./Miniforge3-MacOSX-arm64.sh
chmod +x ./Miniforge3-MacOSX-arm64.sh
sh ./Miniforge3-MacOSX-arm64.sh
rm ./Miniforge3-MacOSX-arm64.sh

conda remove -n sip-venv
conda create --name=sip-venv
conda activate sip-venv

python3 -m pip install --upgrade pip

pip install -r requirements.txt
pip install -e .
