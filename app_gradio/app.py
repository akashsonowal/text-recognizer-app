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

):
  """Creates a gradio.Interface frontend for an image to text function."""
  frontend = gr.Interface()
  return frontend

class PredictorBackend:
  def run(self, image):
    pass

def _make_parser():
  return parser 
  
if __name__ == "__main__":
  parser = _make_parser()
  args = parser.parse_args()
  main(args)