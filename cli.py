from functools import partial

from binomial import Binomial, TwoTailedBinomial, to_float
	
test_type = {"1":"greater", "2":"less", "3":"two tail"}[input("Under the alternative hypothesis has the probability of success: 1) Increased 2) Decreased 3) Don't know  ")]
sig_level = to_float(input("Enter the significance level for the test "))

trial_prob = to_float(input("Under the null hypothesis what is the probability of success for a single trial "))
sample_size = int(input("What is the size of the sample  "))
sample_successes = int(input("How many successes are there in the sample  "))

dist = partial(Binomial, tail=test_type) if test_type != "two tail" else TwoTailedBinomial
b = dist(sample_successes, sample_size, trial_prob, sig_level)

p = b.calc_p()
if p > sig_level:
	print("p=", p, "insufficient evidence to reject null hypothesis")
else:
	print("p=", p, "sufficient evidence to reject null hypothesis")
print(b.get_critical_region())
