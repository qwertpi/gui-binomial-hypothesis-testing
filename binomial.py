from functools import reduce
#the function that is called when you do x * y
from operator import mul

from distribution import Distribution

class InvalidData(Exception):
    pass

def to_float(s):
	"""
	Turns a string into a float regardless of whether the string is a decimal or a fraction
	:param s: String, the string that is being converted to a float
	:returns: Float
	"""
	try:
		return float(s)
	except ValueError: 
		return float(s.split("/")[0]) / float(s.split("/")[1])

def limited_factorial(n, lim):
	"""
	Gives the same answer as doing n!/lim!
	Actually does n * n-1 * n-2 * ... * n-r, where n-r=lim+1

	:param n: Int, must be positive, the number to take the factorial of
	:param lim: Int, must be less than n and must be positive, once n-r reaches this value the multiplication will stop
	
	:returns: Int, the result of the calculation
	"""

	if n < 0 or lim < 0:
		raise InvalidData("n and lim must be positive integers, you passed n=" + str(n) + " and lim=" + str(lim))
	if lim > n:
		raise InvalidData("lim must be less than n, you passed n=" + str(n) + " and lim=" + str(lim))

	#who says you can't mix functional programming and OOP?
	#this is a foldleft on numbers lim+1 to n (inclusive) with initial value 1
	return reduce(mul, range(lim + 1, n + 1), 1)

def factorial(n):
	"""
	Calculates n!
	:param n: Int, must be positive, the number to take the factorial of
	:returns: Int
	"""
	return limited_factorial(n, 0)

def num_combinations(n, r):
	"""
	Does nCr
	Where nCr=n!/(r!*(n-r)!)

	:param n: Int, must be greater than or equal to 1
	:param r: Int, must be less than n
	
	:returns: Int, the result of the calculation
	"""

	if r > n:
		raise InvalidData("r must be less than n, you passed r=" + str(r) + " and n=" + str(n))

	return limited_factorial(n, r) / factorial(n - r)

class Binomial(Distribution):
	"""
	A one tailed Binomial hypothesis test

	
	Attributes
	----------
	No public attributes

	Methods
	-------
	calc_p()
		Calculates the probability of observing the test statistic (or a more extreme value) under the null hypothesis
	calculate_critical_value()
		Calculates the value at which H0 begins to be rejected
	get_critical_region()
		Calls calculate_critical_value() for you and formats the result to be an inequality
	"""
	def __init__(self, test_stat, num_trials, trial_prob, sig_level, tail):
		"""
		:param test_stat: Int, must be greater than or equal to 0 and less than or equal to num_trials, the number of "successes" in your sample
		:param num_trials: Int, must be greater than or equal to 1, the number of trials in your sample
		:param trial_prob: Float, must in the range 0-1, the probability of "success" in a single trial under H0
		:param sig_level: Float, must be in the range 0-1, the significance level you want to conduct the test at
		:param tail: String, must be either either "greater" or "lower", specifies whether you think the probability of "success" has increased or decreased
		"""

		if num_trials < 1:
			raise InvalidData("num_trials must be greater than or equal to 1, you passed " + str(num_trials))
		if test_stat not in range(0, num_trials+1):
			raise InvalidData("test_stat must be in the range 0-num_trials, you passed test_stat=" + str(test_stat) + " and num_trials=" + str(num_trials))

		self.TEST_STAT = test_stat
		self.NUM_TRIALS = num_trials

		if not 0 <= sig_level <= 1 or sig_level < 0 or not 0 <= trial_prob <= 1:
			raise InvalidData("sig_level and trial_prob must both be in the range 0-1, you passed sig_level=" + str(sig_level) + " and trial_prob=" + str(trial_prob))

		self.TRIAL_PROB = trial_prob
		self.SIG_LEVEL = sig_level

		if tail not in ("greater", "less"):
			raise InvalidData("tail must be either 'greater' or 'less', you passed "+tail)	
		self.TAIL = tail.lower()

	
	def __probability(self, x):
		"""
		Calculates the probability of the observed value being equal to x
		:param x: Int, must be greater than or equal to 0 and must be less than num_trials
		:returns: Float, the probability (0-1)
		"""

		if not 0 <= x <= self.NUM_TRIALS:
			raise InvalidData("x must be in the range 0-num_trials, you passed x=" + str(x) + " but num_trials=" + str(self.NUM_TRIALS))

		return num_combinations(self.NUM_TRIALS, x) * (self.TRIAL_PROB ** x) * ((1 - self.TRIAL_PROB) ** (self.NUM_TRIALS - x))

	#calculates less than or equal to
	def __less_than_probability(self):
		"""
		Calculates the probability of the observed value being less than or equal to the TEST_STAT attribute
		:returns: Float, the probability (0-1)
		"""

		return sum(map(self.__probability, range(0, self.TEST_STAT + 1)))

	def __greater_than_probability(self):
		"""
		Calculates the probability of the observed value being greater than or equal to the TEST_STAT attribute
		:returns: Float, the probability (0-1)
		"""

		return sum(map(self.__probability, range(self.TEST_STAT, self.NUM_TRIALS + 1)))
	
	def calc_p(self):
		"""
		Calls either __greater_than_probability or __less_than_probability depending on the value of the tail attribute
		:returns: Float, the probability of the observed value being equal to or more extreme than the TEST_STAT attribute (0-1)
		"""
		return self.__greater_than_probability() if self.TAIL == "greater" else self.__less_than_probability()


	def calculate_critical_value(self, lower=0, upper=None):
		"""
		Tells you what value of test stat produces the largest calc_p without it's calc_p being greater than SIG_LEVEL
		:returns: Int
		"""
		upper = self.NUM_TRIALS if upper is None else upper

		def change_test_stat(new):
			return Binomial(new, self.NUM_TRIALS, self.TRIAL_PROB, self.SIG_LEVEL, self.TAIL)

		if lower > upper:
			raise InvalidData("Lower can't be bigger than upper you fool!")
		middle = lower + ((upper - lower) // 2)

		#if we have whitled it down to only 2 possible values
		if upper - lower <= 1:
			return lower if change_test_stat(lower).calc_p() < self.SIG_LEVEL else upper

		#if currently inside acceptance region for H0
		if change_test_stat(middle).calc_p() > self.SIG_LEVEL:
			return self.calculate_critical_value(lower, middle) if self.TAIL == "less" else self.calculate_critical_value(middle, upper)

		#if currently inside rejection region for H0
		else:
			return self.calculate_critical_value(lower, middle) if self.TAIL == "greater" else self.calculate_critical_value(middle, upper)

	def get_critical_region(self):
		"""
		Returns a string that describes the values of test_stat that result in rejecting H0
		"""
		if self.TAIL == "greater":
			return "Critical region is X≥"+ str(self.calculate_critical_value())
		else: 
			return "Critical region is X≤" + str(self.calculate_critical_value())


class TwoTailedBinomial(Binomial):
	"""
	A two tailed Binomial Distribution

	See the docs for Binomial for info on public attributes and methods
	"""
	def __init__(self, test_stat, num_trials, trial_prob, sig_level):
		expected_mean = num_trials * trial_prob
		if test_stat > expected_mean:
			super().__init__(test_stat, num_trials, trial_prob, sig_level/2, "greater")
		else:
			super().__init__(test_stat, num_trials, trial_prob, sig_level/2, "less")

	def calculate_critical_value(self, lower=0, upper=None):
		def change_tail(new):
			return Binomial(self.TEST_STAT, self.NUM_TRIALS, self.TRIAL_PROB, self.SIG_LEVEL, new)
		lower_critical_value = change_tail("less").calculate_critical_value(lower, upper)
		upper_critical_value = change_tail("greater").calculate_critical_value(lower, upper)
		
		return (lower_critical_value, upper_critical_value)
	def get_critical_region(self):
		lower_critical_value, upper_critical_value = self.calculate_critical_value()
		
		return "Critical region is " + str(lower_critical_value) + "≥X or " + str(upper_critical_value) + "≤X"
