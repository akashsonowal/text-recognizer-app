"""Basic building blocks for convolution models over lines of text."""
class ConvBlock(nn.Module):
  def forward(self, x: torch.Tensor) -> torch.Tensor:
    """Applies the ConvBlock to x.
    
    Parameters
    ----------
    x
       (B, C, H, W) tensor
    
    Returns
    -------
    torch.Tensor
        (B, C, H, W) tensor
    """
    c = self.conv(x)
    r = self.relu(c)
    return r
