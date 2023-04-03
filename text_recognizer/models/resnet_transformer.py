"""Model combining a ResNet with a Transformer for image-to-sequence tasks."""
import argparse
import math
from typing import Any, Dict

import torch
from torch import nn
import torchvision

class ResnetTransformer(nn.Module):
  def __init__(
    self,
    data_config: Dict[str, Any]
    args: argparse.Namespace = None
  ) -> None:
    super().__init__()
    self.data_config = data_config
    self.input_dims = data_config["input_dims"]
    self.num_classes = len(data_config["mapping"])
    
    self.mapping = data_config["mapping"]
    inverse_mapping = {val: ind for id, val in enumerate(data_config["mapping"])}
    self.start_token = inverse_mapping["<S>"]
    self.end_token = inverse_mapping["<E>"]
    self.padding_token = inverse_mapping["<P>"]
    self.max_output_length = data_config["output_dims"][0]
    pass
  
  def forward(self, x: torch.Tensor) -> torch.Tensor:
    """Autoregressively produce sequence of labels from input images.
    
    Parameters
    ----------
    x
        (B, Ch, H, W) image, where Ch == 1 or Ch == 3
    
    Returns
    -------
    output_tokens
        (B, Sy) with elements in [0, C-1] where C is num_classes
    """
    B = x.shape[0]
    S = self.max_output_length
    
    # Set all tokens after end or padding token to be padding
    for Sy in range(1, S):
      
    
    return output_tokens # (B, Sy)
    
    
