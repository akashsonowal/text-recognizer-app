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
  def __init__(self, url):
    if url is not None:
      self.url = url
      self._predict = self._predict_from_endpoint
    else:
      model = ParagraphTextRecognizer()
      self._predict = model.predict 

  def run(self, image):
    pred, metrics = self._predict_with_metrics(image)
    self._log_inference(pred, metrics)
    return pred
  
  def _predict_with_metrics(self, image):
    pred = self._predict(image)
    stats = ImageStat.Stat(image)
    metrics = {
      "image_mean_intensity": stats.mean,
      "image_median": stats.median,
      "image_extrema": stats.extrema,
      "image_area": image.size[0] * image.size[1],
      "pred_length": len(pred),
    }
    return pred, metrics
  
  def _predict_from_endpoint(self, image):

    """Send an image to an endpoint that accepts JSON and return the predicted text.

    The endpoint should expect a base64 representation of the image, encoded as a string,
    under the key "image". It should return the predicted text under the key "pred".

    Parameters
    ----------
    image
        A PIL image of handwritten text to be converted into a string.

    Returns
    -------
    pred
        A string containing the predictor's guess of the text in the image.
    """
    encoded_image = util.encode_b64_image(image)
    headers = {"Content-type": "application/json"}
    payload = json.dumps({"image": "data:image/png;base64," + encoded_image})
    response = requests.post(self.url, data=payload, headers=headers)
    pred = response.json()["pred"]

    return pred
  
  def _log_inference(self):
    pass

def _load_readme(with_logging=False):
  with open(README) as f:
    lines = f.readlines()
    if not with_logging:
      lines = lines[: lines.index("<!-- logging content below -->\n")]
    readme = "".join(lines)
  return readme

def _make_parser():
  return parser 
  
if __name__ == "__main__":
  parser = _make_parser()
  args = parser.parse_args()
  main(args)