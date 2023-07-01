import os 
from typing import List, Optional, Union

import gantry
import gradio as gr 
from gradio.components import Component
from smart_open import open 

from app_gradio import s3_util
from text_recognizer.util import read_b64_string 



