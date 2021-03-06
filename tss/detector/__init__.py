# ==================================================================== #
# File name: __init__.py
# Author: Automation Lab - Sungkyunkwan University
# Date created: 03/27/2021
# ==================================================================== #
from typing import Dict

from munch import Munch

from .detection import Detection
from .detector import Detector
from .yolov5 import YOLOv5

# MARK: - Lookup Table

def get_detector(hparams: Dict, **kwargs) -> Detector:
	"""Get the detector model based on the given hyperparameters.
	
	Args:
		hparams (dict):
			The model's hyperparameters.

	Returns:
		detector (Detector):
			The detector model.
	"""
	hparams = hparams if isinstance(hparams, Munch) else Munch(hparams)
	name    = hparams.name
	
	if name == "yolov5":  # detector :: name
		return YOLOv5(**hparams, **kwargs)
