from pathlib import Path

from loguru import logger
from tqdm import tqdm

from config import settings

# ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
input_path: Path = settings.data_dir / "dataset.csv"
raw_path: Path = settings.raw_dir / "dataset.csv"
processed_path: Path = settings.processed_dir / "dataset.csv"
output_path: Path = settings.output_dir / "plot.png"
# -----------------------------------------

# ---- REPLACE THIS WITH YOUR OWN CODE ----
logger.info("Generating plot from data...")

iterations = 5
for i in tqdm(range(10), total=10):
    if i == iterations:
        logger.info("Something happened for iteration 5.")
logger.success("Plot generation complete.")
# -----------------------------------------
