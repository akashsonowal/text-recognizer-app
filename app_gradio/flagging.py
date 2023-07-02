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
    def __init__(self, application: str, version: Union[int, str, None] = None, api_key: Optional[str] = None):
        """Logs image-to-text data that was flagged in Gradio to Gantry.

        Images are logged to Amazon Web Services' Simple Storage Service (S3).

        The flagging_dir provided to the Gradio interface is used to set the
        name of the bucket on S3 into which images are logged.

        See the following tutorial by Dan Bader for a quick overview of S3 and the AWS SDK
        for Python, boto3: https://realpython.com/python-boto3-aws-s3/

        See https://gradio.app/docs/#flagging for details on how
        flagging data is handled by Gradio.

        See https://docs.gantry.io for information about logging data to Gantry.

        Parameters
        ----------
        application
            The name of the application on Gantry to which flagged data should be uploaded.
            Gantry validates and monitors data per application.
        version
            The schema version to use during validation by Gantry. If not provided, Gantry
            will use the latest version. A new version will be created if the provided version
            does not exist yet.
        api_key
            Optionally, provide your Gantry API key here. Provided for convenience
            when testing and developing locally or in notebooks. The API key can
            alternatively be provided via the GANTRY_API_KEY environment variable.
        """
        self.application = application
        self.version = version 
        gantry.init(api_key=api_key)
    
    def setup(self, components: List[Component], flagging_dir):
        pass 
    
    def flag(self):
        pass 
    
    def _to_gantry(self):
        pass 
    
    def _to_s3(self):
        pass 
    
    def _find_image_and_text_components():
        pass 

def get_api_key() -> Optional[str]:
    """Convenience method for fetching the Gantry API key."""
    api_key = os.environ.get("GANTRY_API_KEY")
    return api_key