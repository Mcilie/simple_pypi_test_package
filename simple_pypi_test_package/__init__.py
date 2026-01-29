"""
EmbeddingGemma-300M model package.

This package contains the google/embeddinggemma-300m model split into chunks
for distribution via PyPI.
"""

import zipfile
import shutil
from pathlib import Path


def get_model_parts_dir() -> Path:
    """Get the directory containing the model part files."""
    return Path(__file__).parent / "model_parts"


def reconstruct_model(output_dir: str, extract: bool = True, keep_zip: bool = False) -> Path:
    """
    Reconstruct the embeddinggemma-300m model from split parts.

    Args:
        output_dir: Directory where the model will be extracted/saved.
        extract: If True, extract the zip contents. If False, just create the zip.
        keep_zip: If True, keep the zip file after extraction.

    Returns:
        Path to the extracted model directory (if extract=True) or zip file (if extract=False).

    Example:
        >>> from simple_pypi_test_package import reconstruct_model
        >>> model_path = reconstruct_model("./models")
        >>> print(model_path)  # ./models/embeddinggemma-300m

        # Then use with sentence-transformers:
        >>> from sentence_transformers import SentenceTransformer
        >>> model = SentenceTransformer(str(model_path))
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    zip_path = output_path / "embeddinggemma-300m.zip"
    model_dir = output_path / "embeddinggemma-300m"

    parts_dir = get_model_parts_dir()

    # Get all part files sorted alphabetically
    part_files = sorted(parts_dir.glob("part_*"))

    if not part_files:
        raise FileNotFoundError(f"No model parts found in {parts_dir}")

    print(f"Reconstructing model from {len(part_files)} parts...")

    # Concatenate all parts into a single zip file
    with open(zip_path, "wb") as outfile:
        for i, part_file in enumerate(part_files, 1):
            print(f"  Processing part {i}/{len(part_files)}: {part_file.name}", end="\r")
            with open(part_file, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    print(f"\nZip file created: {zip_path}")

    if extract:
        print("Extracting model files...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            # Extract to a temp location first
            zf.extractall(output_path)

        # The zip contains model_download/, rename it to embeddinggemma-300m
        extracted_dir = output_path / "model_download"
        if extracted_dir.exists():
            if model_dir.exists():
                shutil.rmtree(model_dir)
            extracted_dir.rename(model_dir)

        print(f"Model extracted to: {model_dir}")

        if not keep_zip:
            zip_path.unlink()
            print("Cleaned up zip file.")

        return model_dir

    return zip_path


def get_model_path(output_dir: str = None) -> Path:
    """
    Get the path to the model, reconstructing if necessary.

    Args:
        output_dir: Directory to extract to. Defaults to ~/.cache/embeddinggemma-300m

    Returns:
        Path to the model directory.
    """
    if output_dir is None:
        output_dir = Path.home() / ".cache" / "embeddinggemma-300m"
    else:
        output_dir = Path(output_dir)

    model_path = output_dir / "embeddinggemma-300m"

    if not model_path.exists():
        return reconstruct_model(str(output_dir))

    return model_path


# For backwards compatibility
print("embeddinggemma-300m model package loaded. Use reconstruct_model() to extract the model.")
