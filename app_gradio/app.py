"""Provide an image of handwritten text and get back out a string!"""
import argparse 
import json 
import logging 
import os 
from pathlib import Path 
from typing import Callable

import warnings 

import gradio as gr 


class PredictorBackend:
  pass
