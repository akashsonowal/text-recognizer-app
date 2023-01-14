"""
Detects a paragraph of text in an input image.

Example usage of script:

  python text_recognizer/paragraph_text_recognizer.py \
    data/tests/a01-077.png
  
  python text_recognizer/paragraph_text_recognizer.py \
    https://fsdl-public-assets.s3-us-west-2.amazonaws.com/paragraphs/a01-077.png
"""
import argparse
from pathlib import Path

STAGED_MODEL_DIR_NAME = Path(__file__).resolve().parent / "artifacts" / "paragraph-text-recognizer"
MODEL_FILE = "model.pt"

class Paragraph_Text_Recognizer:
  """Recognizes a paragraph of text in an image."""

  def __init__(self, model_path=None):
    if model_path is None:
      model_path = STAGED_MODEL_DIR_NAME / MODEL_FILE
    




def main():
  parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  parser.add_argument("filename", type=str, help="Name for an image file. This can be a local path, a URL, a URI from AWS/GCP/Azure storage, an HDFS path, or any other resource locator supported by the smart_open library.")
  args = parser.parse_args()
  
  text_recognizer = Paragraph_Text_Recognizer()
  pred_str = text_recognizer.predict(args.filename)
  print(pred_str)

if __name__ == "__main__":
  main()
