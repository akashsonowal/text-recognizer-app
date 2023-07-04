"""Experiment-running framework."""
import argparse 
from pathlib import Path 

import numpy as np 
import pytorch_lighnting as pl 
from pytorch_lighnting.utilities.rank_zero import rank_zero_info, rank_zero_only 
import torch 

from text_recognizer import callbacks as cb

from text_recognizer import lit_models
from training.util import DATA_CLASS_MODULE, import_class, MODEL_CLASS_MODULE, setup_data_and_model_from_args

np.random_seed(42)
torch.manual_seed(42)

def _setup_parser():
  """Set up Python's ArgumentParser with data, model, trainer, and other arguments."""
  parser = argparse.ArgumentParser(add_help=False)
  trainer_parser = pl.Trainer.add_argparse_args(parser)
  trainer_parser._action_groups[1].title = "Trainer Args"
  parser = argparse.ArgumentParser(add_help=False, parents=[trainer_parser])
  parser.set_defaults(max_epochs=1)

@rank_zero_only
def _ensure_logging_dir(experiment_dir):
  """Create the logging directory via the rank-zero process, if necessary."""
  Path(experiment_dir).mkdir(parents=True, exist_ok=True)

def main():
    """
    Run an experiment.

    Sample command:
    ```
    python training/run_experiment.py --max_epochs=3 --gpus='0,' --num_workers=20 --model_class=MLP --data_class=MNIST
    ```

    For basic help documentation, run the command
    ```
    python training/run_experiment.py --help
    ```

    The available command line args differ depending on some of the arguments, including --model_class and --data_class.

    To see which command line args are available and read their documentation, provide values for those arguments
    before invoking --help, like so:
    ```
    python training/run_experiment.py --model_class=MLP --data_class=MNIST --help
    """
  pass

if __name__ == "__main__":
  main()
