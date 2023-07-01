"""Provide an image of handwritten text and get back out a string!"""
import argparse 
import json 
import logging 
import os 
from pathlib import Path 
from typing import Callable

import warnings 

import gradio as gr 
from PIL import ImageStat
from PIL.Image import Image 
import requests 

from app_gradio.flagging import GantryImageToTextLogger, get_api_key 
from app_gradio.s3_util import make_unique_bucket_name 

from text_recognizer.paragraph_text_recognizer import ParagraphTextRecognizer 
import text_recognizer.util as util 

os.environ["CUDA_VISIBLE_DEVICES"] = "" # don't use gpu

logging.basicConfig(level=logging.INFO)
DEFAULT_APPLICATION_NAME = "text-recognizer"
APP_DIR = Path(__file__).resolve().parent # what is the directory for this application?
FAVICON = APP_DIR / "favicon.png" # path to a small image for display in browser tab and social media
README = APP_DIR / "readme.md" # path to an app readme file in HTML/markdown

DEFAULT_PORT = 11700

def main(args):
  predictor = PredictorBackend(url=args.model_url)
  frontend = make_frontend(
    predictor.run,
    flagging=args.flagging,
    gantry=args.gantry,
    app_name=args.application
  )
  frontend.launch(
    server_name="0.0.0.0",
    server_port=args.port,
    share=True,
    favicon_path=FAVICON,
  )

def make_frontend(
  fn: Callable[[Image], str],
  flagging: bool = False,
  gantry: bool = False,
  app_name: str = "text-recognizer"
):
  """Creates a gradio.Interface frontend for an image to text function."""
  example_dir = Path("text_recognizer") / "tests" / "support" / "paragraphs"
  example_fnames = [elem for elem in os.listdir(example_dir) if elem.endswith(".png")]
  example_paths = [example_dir / fname for fname in example_fnames]
  examples = [[str(path)] for path in example_paths]

  allow_flagging = "never"

  if flagging:
    allow_flagging = "manual"
    api_key = get_api_key()

    if gantry and api_key:
      allow_flagging = "manual"
      flagging_callback = GantryImageToTextLogger(application=app_name, api_key=api_key)
      flagging_dir = make_unique_bucket_name(prefix=app_name, seed=api_key)
    else:
      if gantry and api_key is None:
        warnings.warn("No Gantry API key found, logging to local directory instead.", stacklevel=1)
      flagging_callback = gr.CSVLogger()
      flagging_dir = "flagged"
  else:
    flagging_dir, flagging_callback = None, None
  
  readme = _load_readme(with_logging=allow_flagging == "manual")

  frontend = gr.Interface(
    fn=fn, 
    outputs=gr.components.Textbox(),
    inputs=gr.components.Image(type="pil", label="Handwritten Text"),
    title="📝 Text Recognizer",
    thumbnail=FAVICON,
    description=__doc__,
    article=readme,
    examples=examples,
    cache_examples=False,
    allow_flagging=allow_flagging,
    flagging_option=["incorrect", "offensive", "other"],
    flagging_callback=flagging_callback,
    flagging_dir=flagging_dir
  )

  return frontend

class PredictorBackend:
  """Interface to a backend that serves predictions.

    To communicate with a backend accessible via a URL, provide the url kwarg.

    Otherwise, runs a predictor locally.
    """
  def run(self, image):
    pass

def _make_parser():
  return parser 
  
if __name__ == "__main__":
  parser = _make_parser()
  args = parser.parse_args()
  main(args)