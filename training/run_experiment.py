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

  parser.add_argument(
    "--wandb",
    action="store_true",
    default=False,
    help="If passed, logs experiment results to Weights & Biases. Otherwise logs only to local Tensorboard.",
  )

  parser.add_argument(
    "--profile",
    action="store_true",
    default=False,
    help="If passed, uses the PyTorch Profiler to track computation, exported as a Chrome-style trace.",
  )

  parser.add_argument(
    "--data_class",
    type=str,
    default="MNIST",
    help=f"String identifier for the data class, relative to {DATA_CLASS_MODULE}.",
  )

  parser.add_argument(
    "--model_class",
    type=str,
    default="MLP",
    help=f"String identifier for the model class, relative to {MODEL_CLASS_MODULE}.",
  )

  parser.add_argument(
    "--load_checkpoint", type=str, default=None, help="If passed, loads a model from the provided path."
  )

  parser.add_argument(
    "--stop_early",
    type=int,
    default=0,
    help="If non-zero, applies early stopping, with the provided value as the 'patience' argument."
    + " Default is 0.",
  )

  temp_args = parser.parse_known_args()
  data_class = import_class(f"{DATA_CLASS_MODULE}.{temp_args.data_class}")
  model_class = import_class(f"{MODEL_CLASS_MODULE}.{temp_args.model_class}")

  data_group = parser.add_argument_group("Data Args")
  data_class.add_to_argparse(data_group)

  model_group = parser.add_argument_group("Model Args")
  model_class.add_to_argparse(model_group)

  lit_model_group = parser.add_argument_group("LitModel Args")
  lit_models.BaseLitModel.add_to_argparse(lit_model_group)

  parser.add_argument("--help", "-h", action="help")
  return parser

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
    parser = _setup_parser()
    args = parser.parse_args()
    data, model = setup_data_and_model_from_args(args)

    lit_model_class = lit_models.BaseLitModel

    if args.loss == "Transformer":
      lit_model_class = lit_models.TransformerLitModel
    
    if args.load_checkpoint is not None:
      lit_model = lit_model_class.load_from_checkpoint(args.load_checkpoint, args=args, model=model)
    else:
      lit_model = lit_model_class(args=args, model=model)
    


if __name__ == "__main__":
  main()
