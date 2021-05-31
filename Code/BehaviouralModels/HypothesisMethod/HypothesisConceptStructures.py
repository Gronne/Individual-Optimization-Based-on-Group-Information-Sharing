





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
        self._effect = None
        self._tests = []
        self._effect_score = effect
        self._test_score = 0            #These numbers does not neet to be actual number, but can instead be calculated when requeting them
        self._general_score = 0         #Another approach is to keep them and recalculate them each time a new test is added
        self._difference = None

        self._test_score_hyper_parameter = 5


    def get_info_str(self):
        differences_str = self._difference.get_difference_str() if self._difference != None else None
        return str(f"Effect-score: {self._effect_score}, test-score: {self._test_score}, general-score: {self._general_score}, diff: {differences_str}")

    def get_effect_score(self):
        return self._effect_score

    def get_test_score(self):
        return self._test_score

    def get_general_score(self):
        return self._general_score 

    def _update_test_score(self):   #What is test score even? And is it dependent on the general score?
        #More general hypotheses must have more tests. The score can be above one, but one is the threshold for "no more testing"
        self._test_score = ((len(self._tests) * self._general_score) / self._test_score_hyper_parameter)

    def _update_general_score(self):
        #should get triggered by an update in difference.
        #The more likely each difference is to be found on a map. 
        #More differences makes it less general, even if each diff have a high generality
        #A difference that have a larger range, e.g. all colors, have a high generality. A single color will have a lower generality
        general_score = 0
        for diff in self._difference.get_difference():
            general_score += self._calc_general_sub_score(diff)
        self._general_score = 1 / general_score

    def _calc_general_sub_score(self, diff):
        pass

    def get_difference(self):
        return self._difference

    def update_difference(self, difference):  
        self._difference = difference
        self._update_general_score()
        self._update_test_score()

    def add_test(self, test, in_favor_flag):
        self._tests += [{"test": test, "in_favor": in_favor_flag}]
        self._update_test_score()




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
        self._difference = self._setup_diff(prior_state, posterior_state, difference)        

    def _setup_diff(self, prior_state, posterior_state, difference):
        if prior_state != None and posterior_state != None:
            self._difference = self._get_state_diff(prior_state, posterior_state)
        elif difference != None:
            if isinstance(difference, Difference):
                self._difference = difference.get_difference()
            else:
                self._difference = difference
        else:
            raise Exception("A difference or two states must be given for this constructor to perform the required task")
        return self._difference

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



class Component:    #Component/Structure/Pattern? What is the difference, Because I'm not sure if it is the same. But it may be.
    def __init__(self):
        pass

