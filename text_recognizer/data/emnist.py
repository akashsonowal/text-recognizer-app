"""EMNIST dataset. Downloads from NIST website and saves as .npz file if not already present."""
import json
import os 
from pathlib import Path 
import shutil
from typing import Sequence 
import zipfile 

import h5py
import numpy as np 
import toml 

from text_recognizer.data.base_data_module import _download_raw_dataset, BaseDataModule, load_and_print_info
from text_recognizer.data.util import BaseDataset, split_dataset
import text_recognizer.metadata.emnist as metadata
from text_recognizer.util import temporary_working_directory

class EMNIST(BaseDataModule):
    def __init__(self, args=None):
        super().__init__(args)



def _process_raw_dataset(filename: str, dirname: Path):
    print("Unzipping EMNIST...")
    with temporary_working_directory(dirname):
        from scipy.io import loadmat

if __name__ == "__main__":
    load_and_print_info(EMNIST)
