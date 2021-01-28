from functools import partial
import sys
from PyQt5 import QtWidgets, uic

from binomial import Binomial, TwoTailedBinomial, to_float

def readtail(x):
	global test_type
	test_type = {"Increased":"greater", "Decreased":"less", "Don't know":"two tail"}[x]

def switch_to(curr, new):
	curr.close()
	new()

# pylint: disable=too-few-public-methods    
class ResultWindow(QtWidgets.QWidget):
	def __init__(self):
		try:
			super().__init__()

			global test_type
			global sig_level
			global trial_prob
			global sample_size
			global sample_successes

			dist = partial(Binomial, tail=test_type) if test_type != "two tail" else TwoTailedBinomial

			b = dist(sample_successes, sample_size, trial_prob, sig_level)

			uic.loadUi("result.ui", self)
			self.text.append("Processing...")
			self.show()
			
			p = b.calc_p()
			if p > sig_level:
				self.text.append("p=" + str(p) + ", insufficient evidence to reject null hypothesis")
			else:
				self.text.append("p=" + str(p) + ", sufficient evidence to reject null hypothesis")
			app.processEvents()
			self.text.append(b.get_critical_region() + "\n")
			self.back.clicked.connect(lambda: switch_to(self, ParameterEntryWindow))
			
			#required else python gets overenthusiastic with garbage collection
			self.dummy.clicked.connect(lambda: self.text.append(""))

		#if any of the variables are undefined, go back to the data entry screen
		except NameError as e:
			print(e)
			switch_to(self, ParameterEntryWindow)

# pylint: disable=too-few-public-methods    
class ParameterEntryWindow(QtWidgets.QWidget):
	def parse(self):
		try:
			global sig_level
			global trial_prob
			global sample_size
			global sample_successes

			sig_level = to_float(self.sig_level_input.text())
			trial_prob = to_float(self.trial_prob_input.text())
			sample_size = int(self.sample_size_input.text())
			sample_successes = int(self.num_sucess_input.text())
			switch_to(self, ResultWindow)

		except ValueError:
			pass

	def __init__(self):
		super().__init__()
		uic.loadUi("input.ui", self)
		self.show()
		self.tail_input.currentTextChanged.connect(readtail)
		self.submit.clicked.connect(self.parse)

		#required else python gets overenthusiastic with garbage collection
		self.dummy.clicked.connect(lambda: self.tail_input.append(""))


app = QtWidgets.QApplication(sys.argv)
ParameterEntryWindow()
sys.exit(app.exec_())
