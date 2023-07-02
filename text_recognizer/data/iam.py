def _extract_raw_dataset(filename: str, dirname: Path) -> None:
    print("Extracting IAM data")
    with util.temporary_working_directory(dirname):
        with zipfile.ZipFile(filename, 'r') as zip_file:
            zip_file.extractall()
