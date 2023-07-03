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

def load_and_print_info():
  pass
