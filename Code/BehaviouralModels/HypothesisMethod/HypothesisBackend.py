from BehaviouralModels.HypothesisMethod.HypothesisDBStructures import *
from BehaviouralModels.HypothesisMethod.HypothesisConceptStructures import *




class HypothesisBackend:
    def __init__(self):
        self._agentDB = AgentDB()
        self._hypothesisDB = HypothesisDB()
        self._testDB = TestDB()

    def print_dbs(self):
        self._agentDB.print_db()
        self._hypothesisDB.print_db()
        self._testDB.print_db()


    def create_agent(self, agent_name):
        return self._agentDB.create(agent_name)

    def remove_agent(self, agent_id):
        for hypothesis_id in self._agentDB.get_hypotheses(agent_id):
            self._hypothesisDB.remove_agent(hypothesis_id, agent_id)
        for test_id in self._agentDB.get_tests(agent_id):
            self._testDB.remove_agent(test_id, agent_id)
        self._agentDB.remove_agent(agent_id)


    def create_hypothesis(self, effect_score):
        return self._hypothesisDB.create(effect_score)

    def remove_hypothesis(self, hypothesis_id):
        for test_id in self._hypothesisDB.get_tests(hypothesis_id):
            self._testDB.remove_hypothesis(test_id, hypothesis_id)
        for agent_id in self._hypothesisDB.get_agents(hypothesis_id):
            self._agentDB.remove_hypothesis(agent_id, hypothesis_id)
        self._hypothesisDB.remove_hypothesis(hypothesis_id)


    def create_test(self, prior_state, posterior_state, action):
        return self._testDB.create(prior_state, posterior_state, action)

    def remove_test(self, test_id):
        for hypothesis_id in self._testDB.get_hypotheses(test_id):
            self._hypothesisDB.remove_test(hypothesis_id, test_id)
        for agent_id in self._testDB.get_agents(test_id):
            self._agentDB.remove_hypothesis(agent_id, test_id)
        self._testDB.remove_test(test_id)

    
    def get_agent_tests(self, agent_id):
        return self._agentDB.get_tests(agent_id)

    def get_agent_hypotheses(self, agent_id):
        return self._agentDB.get_hypotheses(agent_id)

    
    def get_test_agents(self, test_id):
        return self._testDB.get_agents(test_id)

    def get_test_hypotheses(self, test_id):
        return self._testDB.get_hypothesis(test_id)

    
    def get_hypothesis_agents(self, hypothesis_id):
        return self._hypothesisDB.get_agents(hypothesis_id)

    def get_hypothesis_tests(self, hypothesis_id):
        return self._hypothesisDB.get_tests(hypothesis_id)

    
    def get_agent(self, agent_id):
        return self._agentDB.get_agent(agent_id)

    def get_test(self, test_id):
        return self._testDB.get_test(test_id)

    def get_hypothesis(self, hypothesis_id):
        return self._hypothesisDB.get_hypothesis(hypothesis_id)


    def get_relevant_hypotheses(self, state):
        #Check which hypotheses that appear in the state
        relevant_hypotheses = []
        for hypothesis_id in self._hypothesisDB.get_all_hypothesis_ids():
            hypothesis = self._hypothesisDB.get_hypothesis(hypothesis_id)
            indexes = self._find_patterns_in_state(state, hypothesis)
            if len(indexes):
                relevant_hypotheses += [hypothesis_id]
        return relevant_hypotheses


    def _find_patterns_in_state(self, state, hypothesis):
        #Check if any component or sub component exist in the state
        for sub_diff in hypothesis.get_difference().get_difference():
            index = sub_diff[0]
            from_state = sub_diff[1]
            if index == '?':
                pass