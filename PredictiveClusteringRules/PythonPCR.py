"""

	created by: masphei @2013
	contact: masphei@gmail.com
	description: Predictive Clustering Rule implemented in python is a clustering algorithm based on rules.
	
"""
# global variable
MAX_TARGET = 2

# Configuration for PlayTennis dataset
WEIGHT_OF_ATTRIBUTES = [4, 2, 1, 3]
TARGET_INDEX = 0 # starting from 0
MINIMUM_EXAMPLES_COVERAGE = 30 # percentage
FILE_NAME = "D:/playtennis.txt"
DATATEST_FILE_NAME = ""

# Configuration for Monk dataset:
# monk 1
# WEIGHT_OF_ATTRIBUTES = [7, 6, 5, 4, 3, 2, 1]
# MINIMUM_EXAMPLES_COVERAGE = 30 # percentage
# FILE_NAME = "D:/Copy/Coding/GitHub/DataMining/PredictiveClusteringRules/monk-1.txt"
# DATATEST_FILE_NAME = "D:/Copy/Coding/GitHub/DataMining/PredictiveClusteringRules/monk-1-test.txt"

# monk 2
# WEIGHT_OF_ATTRIBUTES = [7, 6, 15, 4, 3, 2, 21]
# WEIGHT_OF_ATTRIBUTES = [7, 6, 5, 4, 3, 2, 1]
# MINIMUM_EXAMPLES_COVERAGE = 20 # percentage
# FILE_NAME = "D:/Copy/Coding/GitHub/DataMining/PredictiveClusteringRules/monk-2.txt"
# DATATEST_FILE_NAME = "D:/Copy/Coding/GitHub/DataMining/PredictiveClusteringRules/monk-2-test.txt"

# monk 3
# WEIGHT_OF_ATTRIBUTES = [7, 16, 5, 24, 3, 2, 11]
# MINIMUM_EXAMPLES_COVERAGE = 40 # percentage
# FILE_NAME = "D:/Copy/Coding/GitHub/DataMining/PredictiveClusteringRules/monk-3.txt"
# DATATEST_FILE_NAME = "D:/Copy/Coding/GitHub/DataMining/PredictiveClusteringRules/monk-3-test.txt"

class PythonPCR:
    def __init__(self):
		self.attributes = []
		self.instances = []
		self.list_rules = []
		self.datatest = []
		self.datatest_target = []
		self.target = []
		self.accuracy = 0
		
		self.load_file()
		self.variations = self.init_variations()
		self.learn_rule_set()
		self.cluster_instances()
		
	#input dataset from specified file
    def load_file(self):
		counter_row = 0
		counter_col = 0
		row = []
		instance = ""
		#iterate whole lines
		for line in open(FILE_NAME):
			#iterate each character
			for char in line:
				if char == "\n":
					counter_col += 1
					row.append(instance)
					if len(self.attributes) == 0:
						self.attributes = row
					else:
						self.instances.append(row)
					row = []
					instance = ""
				elif char == ",":
					row.append(instance)
					instance = ""
				else:
					instance += char
		self.attributes.pop()
		for x in self.instances:
			self.target.append(x[TARGET_INDEX])
			x.pop(TARGET_INDEX)
		# print "Attributes: ", self.attributes
		# print "Instance: ", self.instances
		# print "Target: ", self.target
		if DATATEST_FILE_NAME == "":
			print "datatest using dataset"
		else:
			print "datatest is defined"
			for line in open(DATATEST_FILE_NAME):
				#iterate each character
				for char in line:
					if char == "\n":
						counter_col += 1
						row.append(instance)
						if len(self.attributes) != 0:
							self.datatest.append(row)
						row = []
						instance = ""
					elif char == ",":
						row.append(instance)
						instance = ""
					else:
						instance += char
			self.datatest.pop(0)
			for x in self.datatest:
				self.datatest_target.append(x[TARGET_INDEX])
				x.pop(TARGET_INDEX)
			# print "datatest: ", self.datatest, " #",len(self.datatest)
	
    def init_variations(self):
		variations = [([]) for x in self.attributes]
		for x in range(len(self.instances)):
			for y in range(len(self.instances[x])):
				if self.instances[x][y] not in variations[y]:
		
					variations[y].append(self.instances[x][y])
		# print "variations: ", variations
		return variations
	
    def learn_rule_set(self):
		# print "LearnRuleSet"
		list_rules = []
		learning_set = self.init_learning_set()
		self.learning_iteration(learning_set, list_rules)
		while self.stop_learning(learning_set, list_rules) != True:
			self.learning_iteration(learning_set, list_rules)
			
		print "list rules: ", len(list_rules)
		# print "rules:", list_rules
		# list_rules = self.review_rules(list_rules, learning_set)
		# list_rules = self.optimize_rule_set(list_rules)
		self.list_rules = list_rules[:]
	
    def find_candidate_rules(self, learning_set):
		# start with the most general cluster description or condition that satisfied by all examples in Ec
		# then begin specialization of all conditions in the current set of conditions C by conjunctively adding an extra test
		# consider all possible tests that are not already in the condition that we are specializing
		# consider condition that cover at least a predefined minimal number of examples
		rules = []
		value = max(WEIGHT_OF_ATTRIBUTES)
		index = WEIGHT_OF_ATTRIBUTES.index(value)
		
		variations = [([]) for x in self.attributes]
		for x in range(len(learning_set)):
			for y in range(len(learning_set[x])):
				if learning_set[x][y] not in variations[y]:
					variations[y].append(learning_set[x][y])
		# print "variation:", variations
					
		rule = [x for x in variations]
		# iterate whole attributes
		number_of_covered_examples = self.examples_covered(rule, learning_set)
		
		sort_weight = []
		temp_weight = WEIGHT_OF_ATTRIBUTES[:]
		for x in temp_weight:
			value = max(temp_weight)
			index = temp_weight.index(value)
			# print "max:",value
			sort_weight.append(index)
			temp_weight[index] = -1
		# print "sort:",sort_weight
		# print "covered:",number_of_covered_examples
		
		# copy list
		new_rule = []
		for x in rule:
			row = []
			for y in x:
				row.append(y)
			new_rule.append(row)
		
		counter = 0
		
		limit = MINIMUM_EXAMPLES_COVERAGE / float(100) * len(self.instances)
		# print "min examples:", limit
		while number_of_covered_examples > limit:
			# print "new rule ",new_rule
			# if len(new_rule[sort_weight[counter]]>0):
			# print "rule ", rule
			new_rule[sort_weight[counter]].pop(0)
			# print "new rule ", new_rule
			# print "rule ", rule
			number_of_covered_examples = self.examples_covered(new_rule, learning_set)
			if number_of_covered_examples > limit:
				rule[sort_weight[counter]].pop(0)
				# print "copy rule"
				# print "counter:",counter, " covered:", number_of_covered_examples
			counter += 1
			if counter >= len(self.attributes):
				counter = 0
		# print "number of covered", self.examples_covered(rule, learning_set)
		rules.append(rule)
		# print "\ncandidate: ", rules
		return rules
	
    def examples_covered(self, rule, examples):
		instances = 0
		for x in range(len(examples)):
			match = True
			for y in range(len(examples[x])):
				if examples[x][y] not in rule[y]:
					match = False
			if match:
				instances += 1
		return instances
				
    def apply_rules(self, instances, rule):
		counter = len(instances) - 1
		while counter >= 0:
			match = True
			# print counter
			for y in range(len(instances[counter])):
				if instances[counter][y] not in rule[y]:
					match = False
			if match:
				# print "pop ",counter
				instances.pop(counter)
			counter -= 1
		# print "apply learning set: ", len(instances)
	
    def best_rule(self, candidate_rules):
		if len(candidate_rules) > 0:
			return candidate_rules[0]
		else:
			return []
	
    def modify_learning_set(self):
		print "ModifyLearningSet"
	
    def stop_learning(self, learning_set, list_rules):
		if len(learning_set) == 0:
			return True
		if len(list_rules) >= MAX_TARGET:
			return True
		return False
	
    def review_rules(self, list_rules, learning_set):
		return []
	
    def optimize_rule_set(self, list_rules):
		print "OptimizeRuleSet"
	
    def init_learning_set(self):
		return self.instances[:]
		
    def learning_iteration(self, learning_set, list_rules):
		candidate_rules = self.find_candidate_rules(learning_set)
		current_rule = self.best_rule(candidate_rules)
		list_rules.append(current_rule)
		self.apply_rules(learning_set, current_rule)
		# print "learning_set:", learning_set
		# learning_set.remove(learning_set[0])
		# print "current rule: ", current_rule
		# print "learning iteration"
		
    def heuristic_func(self, instance):
		heuristic = 0		
		
		return heuristic
	
    def cluster_instances(self):
		# print "clustering"
		result = []
		choice_of_target = []
		map_result = []
		if len(self.datatest) == 0:
			for x in self.instances:
				for y in range(len(self.list_rules)):
					if self.check_instance(x, self.list_rules[y]):
						result.append(y)
						break
			print result
			for x in self.target:
				if x not in choice_of_target:
					choice_of_target.append(x)
			# print choice_of_target
			for x in self.target:
				map_result.append(choice_of_target.index(x))
			# print map_result
			
			sum = 0
			for x in range(len(result)):
				if result[x] == map_result[x]:
					sum += 1
			percentage = sum * 1.0 / len(result)
			
			self.accuracy = max(1 - percentage, percentage)
			print "accuracy: ", self.accuracy
				
		else:
			for x in self.datatest:
				have_cluster = False
				for y in range(len(self.list_rules)):
					if self.check_instance(x, self.list_rules[y]):
						result.append(y)
						have_cluster = True
						break
				if not have_cluster:
					closest_rule = self.get_closest_rule(x)
					result.append(closest_rule)
					# print "rule for ", y, " is ",closest_rule
			print "result: ", result
			print "num of examples : ", len(result)
			for x in self.datatest_target:
				if x not in choice_of_target:
					choice_of_target.append(x)
			# print choice_of_target
			for x in self.datatest_target:
				map_result.append(choice_of_target.index(x))
			# print map_result
			
			sum = 0
			for x in range(len(result)):
				if result[x] == map_result[x]:
					sum += 1
			percentage = sum * 1.0 / len(result)
			
			self.accuracy = max(1 - percentage, percentage)
			print "accuracy: ", self.accuracy
	
    def get_closest_rule(self, instance):
		index = -1
		value = -9999
		for x in range(len(self.list_rules)):
			sum = 0
			for y in range(len(instance)):
				if instance[y] in self.list_rules[x][y]:
					sum += 1
			if value < sum:
				value = sum
				index = x
		return index
	
    def check_instance(self, instance, rule):
		match = True
		for x in range(len(instance)):
			# print instance[x]
			# print rule[x]
			if instance[x] not in rule[x]:
				match = False
		return match
		

		
# example of usage
pcr = PythonPCR()

def permutList(l):
	if not l:
			return [[]]
	res = []
	for e in l:
			temp = l[:]
			temp.remove(e)
			res.extend([[e] + r for r in permutList(temp)])

	return res
	
# Testing for acquiring the best accuracy from permutation of heuristic
# list = permutList(WEIGHT_OF_ATTRIBUTES)
# acc = 0
# for x in list:
	# pcr = PythonPCR()
	# if acc<pcr.accuracy:
		# acc = pcr.accuracy
# print acc
	