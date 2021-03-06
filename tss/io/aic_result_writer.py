# ==================================================================== #
# File name: aic_result_writer.py
# Author: Automation Lab - Sungkyunkwan University
# Date created: 03/28/2021
# ==================================================================== #
import os
import time
from typing import List
from typing import Optional

from tss.road_objects import GMO
from tss.utils import data_dir
from tss.utils import printe

# MARK: - Global Vars

# The numeric identifier of input camera stream
video_map = {
    "cam_1":      1,
    "cam_7":      16,
}


# MARK: - AICResultWriter

class AICResultWriter(object):
	"""IO class to output the counting results in only ONE camera.
	"""
	
	# MARK: Magic Function
	
	def __init__(
		self,
		camera_name: Optional[str] = None,
		output_dir : Optional[str] = None,
		start_time : float         = 0.0,
		**kwargs
	):
		super().__init__(**kwargs)
		self.output_dir = output_dir if (output_dir is not None) else data_dir
		self.start_time = start_time if (start_time is not None) else time.time()
		
		if camera_name:
			self.video_id = video_map[camera_name]
		else:
			printe(f"The given ``camera_name`` has not been defined in AIC camera list. Please check again!")
			raise ValueError
		
		result_file        = os.path.join(self.output_dir, camera_name + ".txt")
		self.result_writer = open(result_file, "w")
	
	def __del__(self):
		""" Close the writer
		
		Returns:

		"""
		self.result_writer.close()
	
	# MARK: Write
	
	def write_counting_result(
		self,
		vehicles: List[GMO],
	):
		""" Write counting result from a list of tracked vehicles.
		"""
		# TODO: Print all the GMO to the file
		for vehicle in vehicles:
			gen_time = format((vehicle.last_timestamp - self.start_time), ".2f")
			frame_id = vehicle.last_frame_index
			moi_id   = vehicle.moi_uuid
			class_id = vehicle.label_id_by_majority
			if class_id in [1, 2]:
				result_str = f"{gen_time} {self.video_id} {frame_id} {moi_id} {class_id}\n"
				self.result_writer.write(result_str)


# MARK: - Compress result

from operator import itemgetter
def compress_all_result(
	output_dir : Optional[str] = None,
	output_name: Optional[str] = None
):
	"""  Compress all result of video into one file
	"""
	output_dir      = output_dir  if (output_dir is not None) else data_dir
	output_name     = output_name if (output_name is not None) else "track1"
	output_name     = os.path.join(output_dir, f"{output_name}.txt")
	compress_writer = open(output_name, "w")
	
	# TODO: Get result from each file
	
	for video_name, video_id in video_map.items():
		video_result_path = os.path.join(output_dir, f"{video_name}.txt")
		
		if not os.path.exists(video_result_path):
			printe(f"The result of {video_result_path} is not exist")
			continue
			
		# TODO: Read result
		results = []
		with open(video_result_path) as f:
			line = f.readline()
			while line:
				words = line.split(' ')
				result = {
					"gen_time"   : float(words[0]),
					"video_id"   : int(words[1]),
					"frame_id"   : int(words[2]),
					"movement_id": int(words[3]),
					"class_id"   : int(words[4]),
				}
				if result["class_id"] != 0:
					results.append(result)
				line = f.readline()
				

		# TODO: Sort result
		results = sorted(results, key=itemgetter("gen_time", "frame_id", "movement_id"))

		# TODO: write result
		for result in results:
			compress_writer.write(f"{result['gen_time']} ")
			compress_writer.write(f"{result['video_id']} ")
			compress_writer.write(f"{result['frame_id']} ")
			compress_writer.write(f"{result['movement_id']} ")
			compress_writer.write(f"{result['class_id']}")
			compress_writer.write("\n")

	compress_writer.close()
