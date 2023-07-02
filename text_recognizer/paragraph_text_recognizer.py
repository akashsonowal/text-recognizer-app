"""Detects a paragraph of text in an input image.

Example usage as a script:

  python text_recognizer/paragraph_text_recognizer.py \
    text_recognizer/tests/support/paragraphs/a01-077.png

  python text_recognizer/paragraph_text_recognizer.py \
    https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png
"""
import argparse 
from pathlib import Path
from typing import Sequence, Union

from PIL import Image 
import torch 

from text_recognizer import util
from text_recognizer.stems.paragraph import ParagraphStem 

STAGED_MODEL_DIRNAME = Path(__file__).resolve().parent / "artifacts" / "paragraph-text-recognizer"
MODEL_FILE = "model.pt"

class ParagraphTextRecognizer():
    def __init__(self):
        pass 
    
    def predict(self):
        pass

def main():
    text_recognizer = ParagraphTextRecognizer()
    pred_str = text_recognizer.predict(args.filename)
    print(pred_str)

if __name__ == "__main__":
    main()
