





class Agent:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_info_str(self):
        return str(f"Name: {self._name}")





class Hypothesis:
    def __init__(self, effect):
        self._cause = None
        self._tests = []
        self._effect_score = effect
        self._test_score = 0
        self._general_score = 0
        self._difference = None

    def get_info_str(self):
        return str(f"None")

    def get_effect_score(self):
        return self._effect_score

    def get_test_score(self):
        return self._test_score

    def get_general_score(self):
        #The general score should be determined based on how new differences there are and how wide of a range that the difference has
        return self._general_score 




class Test:
    def __init__(self, prior_state, posterior_state, action):
        self._prior_state = prior_state
        self._posterior_state = posterior_state
        self._action = action
        self._difference = Difference(self._prior_state, self._posterior_state)

    def get_info_str(self):
        differences_str = self._difference.get_difference_str()
        return str(f"Diff: {differences_str}, Action: {self._action}")

    def get_prior_state(self):
        return self._prior_state

    def get_posterior_state(self):
        return self._posterior_state

    def get_action(self):
        return self._action

    def get_difference(self):
        return self._difference

    def get_nr_of_diffs(self):
        return self._difference.get_nr_of_diffs()




class Difference:
    def __init__(self, prior_state = None, posterior_state = None, difference = None):
        if prior_state != None and posterior_state != None:
            self._difference = self._get_state_diff(prior_state, posterior_state)
        elif difference != None:
            if isinstance(difference, Difference):
                self._difference = difference.get_difference()
            else:
                self._difference = difference
        else:
            raise Exception("A difference or two states must be given for this constructor to perform the required task")

    def get_difference(self):
        return self._difference

    def get_difference_str(self):
        diff_str = "".join(str(diff[0]) + " " + str(diff[1]) + "->" + str(diff[2]) + ", " for diff in self._difference)[:-2]
        return diff_str

    def _get_state_diff(self, prior_state, posterior_state): #Recursive
        differences = []
        for index, element in enumerate(prior_state):
            if isinstance(element, list): 
                recursive_diffs = self._get_state_diff(prior_state[index], posterior_state[index])
                for count, diff in enumerate(recursive_diffs):
                    recursive_diffs[count] = ([index] + diff[0], diff[1], diff[2]) 
                differences += recursive_diffs
            elif prior_state[index] != posterior_state[index]:
                diff = ([index], prior_state[index], posterior_state[index])
                differences += [diff]
        return differences

    def remove_part(self, index):
        self._difference = self._difference[:index] + self._difference[index+1:]

    def get_diff_subset(self, subset_list):
        return Difference(difference = [diff for index, diff in enumerate(self._difference) if index in subset_list])

    def get_nr_of_diffs(self):
        return len(self._difference)

