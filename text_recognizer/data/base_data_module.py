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

BATCH_SIZE = 128
NUM_AVAIL_CPUS = len(os.sched_getaffinity(0))
NUM_AVAIL_GPUS = torch.cuda.device_count()

# sensible multiprocessing defaults: at most one worker per CPU
DEFAULT_NUM_WORKERS = NUM_AVAIL_CPUS
# but in distributed data parallel mode, we launch a training on each GPU, so must divide out to keep total at one worker per CPU
DEFAULT_NUM_WORKERS = NUM_AVAIL_CPUS // NUM_AVAIL_GPUS if NUM_AVAIL_GPUS else DEFAULT_NUM_WORKERS

class BaseDataModule(pl.LightningDataModule):
  """Base for all of our LightningDataModules.

  Learn more at about LDMs at https://pytorch-lightning.readthedocs.io/en/stable/extensions/datamodules.html
  """
  def __init__(self, args: argparse.Namespace = None) -> None:
    super().__init__()
    self.args = vars(args)
  
  def config():
    pass 
    
  def prepare_data():
    pass 

  def setup():
    pass
  
  def train_dataloader(self):
    pass 
  
  def val_dataloader(self):
    pass 
  
  def test_dataloader(self):
    pass 
