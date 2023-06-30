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



class PredictorBackend:
  pass
