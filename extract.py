# extract.py

"""
	This script extracts all of the .zip and .tar.gz files downloaded from the google drive
	containing all of the WiFi logs. 

	The log data is all compressed in a .tar.gz file. When downloading from google drive, 
	google will automatically zip files less than 2gb with other files before downloaded.
	Files that are larger (greather than 2gb) will just be downloaded as is (.tar.gz). 
	So our actual directory will contain a mix of both .zip (containing .tar.gz) and .tar.gz.
	The script handles this accordingly.

	As the files are decompressed they are written to a new location and then the original
	compressed file (either .zip or .tar.gz) will be deleted. 

	The script utilizes the multiprocessing module for parallelization. Since there is so
	much data, the process will take time. Parallelizing the data will speed up the process
	depending on the number of workers assigned.
"""

import os
import time 
import logging
from pathlib import Path
from zipfile import ZipFile
from tarfile import TarFile
from multiprocessing import Pool

DATA_PATH = Path('/media/calvinhathcock/Secondary SSD/ITSC_4155_Capstone/drive_zip')
DEST_PATH = Path('/media/calvinhathcock/Secondary SSD/ITSC_4155_Capstone/dataset/raw/wifi')
LOG_PATH = Path('/media/calvinhathcock/Secondary SSD/ITSC_4155_Capstone/dataset/logs')

logging.basicConfig(filename= LOG_PATH / Path('extraction_log.log'), encoding='utf-8', level=logging.INFO)

def unpack_tar(file):
	"""
		Given a file object, open with TarFile and extract to destination
	"""
	with TarFile(fileobj = file) as tf:
		tf.extract(tf.getmembers()[0], path = DEST_PATH)

def unpack_tar_from_path(tar_path: Path):
	"""
		Given a file path, open with TarFile and extract to destination
	"""
	with TarFile(DATA_PATH / tar_path) as tf:
		tf.extract(tf.getmembers()[0], path = DEST_PATH)

def unpack(f: str):
	"""
		Extract the compressed file.

		Given a path to a file f:
			if the file is a zip:
				use ZipFile to open it,
				for each tar file in the zip,
					unpack the tar file and write to disk
			if the file is a tar
				unpack the tar file and write to disk

	"""
	logging.info(f'{f} is being extracted')

	if "Student_" in f:	# All zip files in the directory start with 'Student_'
		with ZipFile(DATA_PATH / Path(f), 'r') as zip_obj:
			for zf in zip_obj.namelist():
				with zip_obj.open(zf) as myfile:
					unpack_tar(myfile)

		logging.info(f'{f} is being deleted')

		os.remove(DATA_PATH / Path(f)) 	#delete file once extracted
	else:	# if not a zip, only other option is .tar.gz
		unpack_tar_from_path(Path(f))

		logging.info(f'{f} is being deleted')

		os.remove(DATA_PATH / Path(f))	#delete file once extracted


if __name__  == "__main__":

	starttime = time.time()

	logging.info(f'Beginning extraction process at {starttime}')

	os.chdir(DATA_PATH)

	files = os.listdir(DATA_PATH)

	logging.info(f'Files to be extracted: {files}')

	pool = Pool()
	pool.map(unpack, files)
	pool.close()

	endtime = time.time()

	logging.info(f'Finishing extraction process at {endtime}')