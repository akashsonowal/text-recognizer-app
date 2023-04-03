"""Model combining a ResNet with a Transformer for image-to-sequence tasks."""
import argparse
import math
from typing import Any, Dict

import torch
from torch import nn
import torchvision

from .transformer_util

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
    x = self.encode(x) # (Sx, B, E)
    
    output_tokens = (torch.ones((B, S)) * self.padding_token).type_as(x).long() #(B, Sy)
    output_tokens[:, 0] = self.start_token # Set start token
    for Sy in range(1, S):
      y = output_tokens[:, :Sy] # (B, Sy)
      output = self.decode(x, y) # (Sy, B, C)
      output = torch.argmax(output, dim=-1) # (Sy, B)
      output_tokens[:, Sy] = output[-1] # Set the last output token
      
      # Early stopping of prediction loop to speed up prediction
      if ((output_tokens[:, Sy] == self.end_token) | (output_tokens[:, Sy] == self.padding_token)).all:
        break
    
    # Set all tokens after end or padding token to be padding
    for Sy in range(1, S):
      ind = (output_tokens[:, Sy-1] == self.end_token) | (output_tokens[:, Sy-1] == self.padding_token)
      output_tokens[ind, Sy] = self.padding_token
    
    return output_tokens # (B, Sy)
      
    
    return output_tokens # (B, Sy)
  
  def encode(self, x: torch.Tensor) -> torch.Tensor:
    """Encode each image tensor in a batch into a sequence of embeddings.
      
    Parameters
    ----------
    x 
        (B, Ch, H, W) image, where Ch == 1 or Ch == 3
        
    Returns
    -------
        (Sx, B, E) sequence of embeddings, going left-to-right, top-to-bottom from final resnet feature maps
    """
    pass
  
  def decode(self, x, y):
    """"""
    pass
