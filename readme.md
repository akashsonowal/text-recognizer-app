# text-recognizer-app

![](app_diagram.png)
Note: This repo is a full clone of the fsdl text recognizer app. All credit goes to [fsdl](https://github.com/full-stack-deep-learning/fsdl-text-recognizer-2022). I have cloned this repo for my own learning exercise.

## Usage

### 1. Check out the repo
```
git clone https://github.com/akashsonowal/text-recognizer-app.git && cd text-recognizer-app
```
### 2. Set up the Python environment
Install python and CUDA 
```
make conda-update
conda activate text-recognizer-app
```
Install python packages
```
make pip-tools
```
Set PYTHONPATH
```
echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc
```
### 3. Setup and prepare data
- EMNIST: The raw data is a .mat file which is processed to .h5 file. The metadata file is downloaded in a .toml file.
