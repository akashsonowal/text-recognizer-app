# text-recognizer-app

![](app_diagram.png)
Note: This repo is a full clone of the fsdl text recognizer app. All credit goes to [fsdl](https://github.com/full-stack-deep-learning/fsdl-text-recognizer-2022). I have cloned this repo for my own learning exercise.

## Repo Structure
- .aws/config - contains the configs for AWS CLI to access AWS resources
- .devcontainer/ - different devcontainer.json for containerized development work in VSCode
  

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
- For all datasets, the metadata was provided in "data/raw/*"
- EMNIST: The data is downloaded (by matching the sha256) to a "data/downloaded/emnist/matlab.zip" which has a *.mat file that is processed (class balancing and augment characters) to a .h5 file in "data/processed/emnist/"
- EMNISTLines (NUM_TRAIN = 10000, NUM_VAL = 2000, NUM_TEST = 2000): default len is 32, min_overlap: 0, max_overlap: 0.33. Here in preparing data we generate lines. To generate lines, we first create labels from a brown text sentence generator. Also, for variation in the images, we maintain a character level for different images of the same character which we uniformly sample to stitch together the images. And finally, we process to store it in a .h5 file. In setup, we set up our data loaders.
- EMNISTLines2 (same except the max_length: 43, min_overlap: 0.2, max_overlap: 0.5) and with padding to match for the emnist_lines 2 metadata.
- FakeData is from torch *just for fun)
- IAM: The labels are in xml files inside downloaded/iam/iamdb/xml/*.xml after extracting zip. The images are in downloaded/iam/iamdb/forms/*.jpg. The splits are also provided in downloaded/iam/iamdb/task/testset.txt

## Results
- Best Loss:
  - train loss: 0.0103; val loss: 0.0208; test loss: 0.7666
- Best cer:
  - val cer: 0.0247, test cer: 0.1293
