"""
This is probably what you actually want to read and write to.
These present something that is almost totally like a numpy
array, so you can operate on it very very quickly with numpy
operations.
"""

import logging
import os
import numpy as np
import mmap
import skyscreen_core.interface


class BaseMMapInterface(object):
	def __init__(self, shared_file):
		self.shared_file = shared_file
		self.shared_memory = None

	def __exit__(self, type, value, traceback):
		assert self.shared_memory is not None, 'already closed, or never opened'
		del self.shared_memory

class NPMMAPScreenWriter(BaseMMapInterface, skyscreen_core.interface.ScreenWriter):
	file_mode = os.O_RDWR

	def __init__(self, shared_file):
		super(NPMMAPScreenWriter, self).__init__(shared_file)

	def initialize_file(self):
		array = np.memmap(self.shared_file,
						  dtype=np.byte,
						  mode='w+',
						  shape=(self.screen_vane_count*self.screen_vane_length*3))
		return array

	def __enter__(self):
		assert self.shared_memory is None, 'cannot open shared mem twice'
		self.shared_memory = np.memmap(self.shared_file,
						  dtype=np.byte,
						  mode='w+',
						  shape=(self.screen_vane_count*self.screen_vane_length*3))
		return self.shared_memory

class NPMMAPScreenReader(BaseMMapInterface, skyscreen_core.interface.ScreenWriter):
	def __init__(self, shared_file):
		super(NPMMAPScreenReader, self).__init__(shared_file)

	def initialize_file(self):
		array = np.memmap(self.shared_file,
						  dtype=np.byte,
						  mode='r',
						  shape=(self.screen_vane_count*self.screen_vane_length*3))
		return array

	def __enter__(self):
		assert self.shared_memory is None, 'cannot open shared mem twice'
		self.shared_memory = self.initialize_file()
		return self.shared_memory