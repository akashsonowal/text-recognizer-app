"""Base DataModule class."""
import argparse 
import os 
from pathlib import Path 
from typing import Collection, Dict, Optional, Tuple, Union

import pytorch_lightning as pl 
import torch 
from torch.utils.data import ConcatDataset, DataLoader 

from text_recognizer import util 
from text_recognizer.data.util import BaseDataset
import text_recognizer.metadata.shared as metadata 

def load_and_print_info(data_module_class) -> None:
  """Load EMNISTLines and print info."""
  parser = argparse.ArgumentParser()
  data_module_class.add_to_argparse(parser)
  args = parser.parse_args()
  dataset = data_module_class(args)
  dataset.prepare_data()
  dataset.setup()
  print(dataset)

def _download_raw_dataset(metadata: Dict, dl_dirname: Path) -> Path:
  dl_dirname.mkdir(parents=True, exist_ok=True)
  filename = dl_dirname / metadata["filename"]
  if filename.exists():
    return filename 
  print(f"Downloading raw dataset from {metadata['url']} to {filename} ...")
  util.download_url(metadata['url'], filename)
  print("Computing SHA-256...")
  sha256 = util.compute_sha256(filename)
  if sha256 != metadata["sha256"]:
    raise ValueError("Downloaded data file SHA-256 does not match that listed in metadata document.")
  return filename
