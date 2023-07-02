"""Utility functions for text_recognizer module."""
import base64
import contextlib
import hashlib
from io import BytesIO

import os 
from pathlib import Path 
from typing import Union 
from urllib.request import urlretrieve

import numpy as np 
from PIL import Image 
import smart_open
from tqdm import tqdm

def to_categorical(y, num_classes):
  """1-hot encode a tensor."""
  return np.eye(num_classes, dtype="uint8")[y]

def read_image_pil():
  pass

@contextlib.contextmanager
def temporary_working_directory(working_dir: Union[str, Path]):
  """Temporarily switches to a directory, then returns to the original directory on exit."""
  curdir = os.getcwd()
  os.chdir(working_dir)
  try:
    yield
  finally:
    os.chdir(curdir)
