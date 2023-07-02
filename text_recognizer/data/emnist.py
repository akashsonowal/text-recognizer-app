from text_recognizer.util import temporary_working_directory

def _process_raw_dataset(filename: str, dirname: Path):
    print("Unzipping EMNIST...")
    with temporary_working_directory(dirname):
        from scipy.io import loadmat

