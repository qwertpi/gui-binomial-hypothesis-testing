from binomial import Binomial, TwoTailedBinomial, InvalidData, factorial, limited_factorial, num_combinations
import binomial

from pytest import approx, raises

class TestFactorials():
	def test_simple_zero(self):
		assert factorial(0) == 1
	def test_simple_one(self):
		assert factorial(1) == 1
	def test_simple_five(self):
		assert factorial(5) == 120

	def test_ten_lim_three(self):
		assert limited_factorial(10, 3) == 604800
	def test_11_lim_eight(self):
		assert limited_factorial(11, 8) == 990


class TestNumCombinations():
	def test_chose_zero(self):
		assert num_combinations(5, 0) == 1
	def test_chose_all(self):
		assert num_combinations(7, 7) == 1
	def test_nine_chose_six(self):
		assert num_combinations(9, 6) == 84

	def test_r_greater_than_n(self):
		with raises(InvalidData):
			num_combinations(6, 8)

class TestFactorialsInvalidData():
	def test_negative_n(self):
		with raises(InvalidData):
			factorial(-3)
	def test_negative_lim(self):
		with raises(InvalidData):
			limited_factorial(10, -3)
	def test_lim_bigger_than_n(self):
		with raises(InvalidData):
			limited_factorial(4, 6)

class TestDecrease():
	def test_prob(self):
		dist = Binomial(11, 24, 0.65, 0.025, "less")
		assert dist.calc_p() == approx(0.042253075)
	def test_critical_val(self):
		dist = Binomial(11, 24, 0.65, 0.025, "less")
		assert dist.get_critical_region() == "Critical region is X≤10"

class TestIncrease():
	def test_prob(self):
		dist = Binomial(116, 200, 0.5, 0.05, "greater")
		assert dist.calc_p() == approx(0.014062704)
	def test_critical_val(self):
		dist = Binomial(116, 200, 0.5, 0.05, "greater")
		assert dist.get_critical_region() == "Critical region is X≥113"

class TestTwoTail():
	def test_prob_increase(self):
		dist = TwoTailedBinomial(25, 40, 0.8, 0.02)
		assert dist.calc_p() == approx(0.0079158539)
	def test_critical_val_increase(self):
		dist = TwoTailedBinomial(25, 40, 0.8, 0.02)
		assert dist.get_critical_region() == "Critical region is 25≥X or 38≤X"
	def test_prob_decrease(self):
		dist = TwoTailedBinomial(20, 30, 0.5, 0.005)
		assert dist.calc_p() == approx(0.04936857)
	def test_critical_val_decrease(self):
		dist = TwoTailedBinomial(20, 30, 0.5, 0.005)
		assert dist.get_critical_region() == "Critical region is 6≥X or 24≤X"

class TestBinomialInvalidData():
	def test_no_invalid_data(self):
		Binomial(5, 10, 0.5, 0.1, "greater")

	def test_tail(self):
		with raises(InvalidData):
			Binomial(5, 10, 0.5, 0.1, "blah")

	def test_negative_sample_size(self):
		with raises(InvalidData):
			Binomial(5, -10, 0.5, 0.1, "greater")
	def test_num_successes_greater_than_sample_size(self):
		with raises(InvalidData):
			Binomial(25, 10, 0.5, 0.1, "greater")

	def test_negative_sig_level(self):
		with raises(InvalidData):
			Binomial(5, 10, 0.5, -0.1, "greater")
	def test_sig_level_greater_than_1(self):
		with raises(InvalidData):
			Binomial(5, 10, 0.5, 1.1, "greater")

	def test_negative_prob(self):
		with raises(InvalidData):
			Binomial(5, 10, -0.5, 0.1, "greater")
	def test_prob_greater_than_1(self):
		with raises(InvalidData):
			Binomial(5, 10, 1.3, 0.1, "greater")

	def test_critical_val_lower_bigger_than_upper(self):
		dist = Binomial(116, 200, 0.5, 0.05, "greater")
		with raises(InvalidData):
			Binomial(5, 10, 0.5, 0.1, "greater").calculate_critical_value(100, 50)

