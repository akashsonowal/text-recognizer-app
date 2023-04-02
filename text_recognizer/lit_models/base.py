"""Basic LightningModules on which other modules can be built."""
import argparse

import pytorch_lightning as pl
import torch

class BaseLitModel(pl.LightningModule):
   """
   Generic PyTorch-Lightning class that must be initialized with a PyTorch module.
   """
   pass
