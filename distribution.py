#abstract base class
from abc import ABC

class Distribution(ABC):
	def calculate_critical_region(self):
		"""
		Should return either a single number or a tuple of numbers
		"""
		raise NotImplementedError
	def get_critical_region(self):
		"""
		Should return a string containing an inequality formed by calling calculate_critical_region
		"""
		raise NotImplementedError
	def calc_p(self):
		"""
		Should return a float that is the probability of the observed value occurring under H0
		"""
		raise NotImplementedError
