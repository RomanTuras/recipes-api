import logging
# from pathlib import Path

logger = logging.getLogger("recipe-api")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch.setFormatter(formatter)
logger.addHandler(ch)

# BASE_DIR = Path(__file__).parent.parent
# Only '/tmp' directory has write access, while using Vercel
# fh = logging.FileHandler(BASE_DIR / "tmp" / "recipes-api.log")
# fh.setLevel(logging.ERROR)
# fh.setFormatter(formatter)

# logger.addHandler(fh)
