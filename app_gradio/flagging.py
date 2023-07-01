import os 
from typing import List, Optional, Union

import gantry
import gradio as gr 
from gradio.components import Component
from smart_open import open 

from app_gradio import s3_util
from text_recognizer.util import read_b64_string 

class GantryImageToTextLogger(gr.FlaggingCallback):
    """A FlaggingCallback that logs flagged image-to-text data to Gantry via S3."""
    pass 

def get_api_key() -> Optional[str]:
    """Convenience method for fetching the Gantry API key."""
    api_key = os.environ.get("GANTRY_API_KEY")
    return api_key