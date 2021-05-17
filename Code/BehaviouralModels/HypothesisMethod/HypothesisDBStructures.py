import random

from BehaviouralModels.HypothesisMethod.HypothesisConceptStructures import *


class AgentDB:
    def __init__(self):
        self._db = {}

    def print_db(self):
        print("------------------ Agent DB -----------------")
        for key in self._db:
            agent_id = self._db[key]["Id"]
            agent_info = self._db[key]["Agent"].get_info_str()
            hypothesis_ids = [self._db[key]["Hypotheses"][id] for id in self._db[key]["Hypotheses"]]
            test_ids = [self._db[key]["Tests"][id] for id in self._db[key]["Tests"]]
            print("")
            print(f"Agent = Id: {agent_id}, Info: {agent_info}")
            print(f"Hypotheses: {hypothesis_ids}")
            print(f"Tests: {test_ids}")
            print("")
        print("---------------------------------------------")
        print("")
        print("")
        print("")

    def create(self, agent_name):
        rand_id = random.randint(0, 1000000000)
        while rand_id in self._db and self._db[rand_id].get_name() != agent_name:   #Create a new id if there already is a different agent with that id
            rand_id = random.randint(0, 1000000000)
        self._db[rand_id] = self._create_new_entry(rand_id, agent_name)
        return rand_id

    def _create_new_entry(sel, id, agent_name):
        return {"Id": id, "Agent": Agent(agent_name), "Hypotheses": {}, "Tests": {}}

    def add_hypothesis(self, agent_id, hypothesis_id):
        self._db[agent_id]["Hypotheses"][hypothesis_id] = {"Id": hypothesis_id}

    def add_test(self, agent_id, test_id):
        self._db[agent_id]["Tests"][test_id] = {"Id": test_id}

    def get_hypotheses(self, agent_id):
        return [id for id in self._db[agent_id]["Hypotheses"]] if agent_id in self._db else None

    def get_tests(self, agent_id):
        return [id for id in self._db[agent_id]["Tests"]] if agent_id in self._db else None
    
    def remove_hypothesis(self, agent_id, hypothesis_id):
        del self._db[agent_id]["Hypotheses"][hypothesis_id]

    def remove_test(self, agent_id, test_id):
        del self._db[agent_id]["Tests"][test_id]

    def remove_agent(self, agent_id):
        del self._db[agent_id]

    def get_all_agent_ids(self):
        return [key for key in self._db]

    def get_all_hypothesis_ids(self):
        return list(set([hypothesis_id for key in self._db for hypothesis_id in self._db[key]["Hypotheses"]]))

    def get_all_test_ids(self):
        return list(set([hypothesis_id for key in self._db for hypothesis_id in self._db[key]["Tests"]]))

    def get_agent(self, agent_id):
        return self._db[agent_id] if agent_id in self._db else None








class HypothesisDB:
    def __init__(self):
        self._db = {}

    def print_db(self):
        print("--------------- Hypothesis DB ---------------")
        for key in self._db:
            hypothesis_id = self._db[key]["Id"]
            hypothesis_info = self._db[key]["Hypothesis"].get_info_str()
            test_ids = [self._db[key]["Tests"][id] for id in self._db[key]["Tests"]]
            agent_ids = [self._db[key]["Agents"][id] for id in self._db[key]["Agents"]]
            print("")
            print(f"Hypothesis = Id: {hypothesis_id}, Info: {hypothesis_info}")
            print(f"Tests: {test_ids}")
            print(f"Agents: {agent_ids}")
            print("")
        print("---------------------------------------------")
        print("")
        print("")
        print("")

    def create(self):
        rand_id = random.randint(0, 1000000000)
        while rand_id in self._db:
            rand_id = random.randint(0, 1000000000)
        self._db[rand_id] = self._create_new_entry(rand_id)
        return rand_id

    def _create_new_entry(self, id):
        return {"Id": id, "Hypothesis": Hypothesis(), "Tests": {}, "Agents": {}}

    def add_test(self, hypothesis_id, test_id):
        self._db[hypothesis_id]["Tests"][test_id] = {"Id": test_id, "Support": None}

    def add_agent(self, hypothesis_id, agent_id):
        self._db[hypothesis_id]["Agents"][agent_id] = {"Id": agent_id}

    def get_tests(self, hypothesis_id):
        return [id for id in self._db[hypothesis_id]["Tests"]] if hypothesis_id in self._db else None

    def get_agents(self, hypothesis_id):
        return [id for id in self._db[hypothesis_id]["Agents"]] if hypothesis_id in self._db else None
    
    def remove_test(self, hypothesis_id, test_id):
        if test_id in self._db[hypothesis_id]["Tests"]:
            del self._db[hypothesis_id]["Tests"][test_id]

    def remove_agent(self, hypothesis_id, agent_id):
        if agent_id in self._db[hypothesis_id]["Agents"]:
            del self._db[hypothesis_id]["Agents"][agent_id]

    def remove_hypothesis(self, hypothesis_id):
        if hypothesis_id in self._db:
            del self._db[hypothesis_id]
    
    def get_all_agent_ids(self):
        return list(set([hypothesis_id for key in self._db for hypothesis_id in self._db[key]["Agents"]]))

    def get_all_hypothesis_ids(self):
        return [key for key in self._db]

    def get_all_test_ids(self):
        return list(set([hypothesis_id for key in self._db for hypothesis_id in self._db[key]["Tests"]]))

    def get_hypothesis(self, hypothesis_id):
        return self._db[hypothesis_id] if hypothesis_id in self._db else None









class TestDB:
    def __init__(self):
        self._db = {}

    def print_db(self):
        print("------------------ Test DB ------------------")
        for key in self._db:
            test_id = self._db[key]["Id"]
            test_info = self._db[key]["Test"].get_info_str()
            hypothesis_ids = [self._db[key]["Hypotheses"][id] for id in self._db[key]["Hypotheses"]]
            agent_ids = [self._db[key]["Agents"][id] for id in self._db[key]["Agents"]]
            print("")
            print(f"Test = Id: {test_id}, Info: {test_info}")
            print(f"Hypotheses: {hypothesis_ids}")
            print(f"Agents: {agent_ids}")
            print("")
        print("---------------------------------------------")
        print("")
        print("")
        print("")

    def create(self, prior_state, posterior_state, action):
        rand_id = random.randint(0, 1000000000)
        while rand_id in self._db:
            rand_id = random.randint(0, 1000000000)
        self._db[rand_id] = self._create_new_entry(rand_id, prior_state, posterior_state, action)
        return rand_id

    def _create_new_entry(self, id, prior_state, posterior_state, action):
        return {"Id": id, "Test": Test(prior_state, posterior_state, action), "Hypotheses": {}, "Agents": {}}

    def add_hypothesis(self, test_id, hypothesis_id):
        self._db[test_id]["Hypotheses"][hypothesis_id] = {"Id": hypothesis_id}

    def add_agent(self, test_id, agent_id):
        self._db[test_id]["Agents"][agent_id] = {"Id": agent_id}

    def get_hypothesis(self, test_id):
        return [id for id in self._db[test_id]["Hypotheses"]] if test_id in self._db else None

    def get_agents(self, test_id):
        return [id for id in self._db[test_id]["Agents"]] if test_id in self._db else None
    
    def remove_hypothesis(self, test_id, hypothesis_id):
        if hypothesis_id in self._db[test_id]["Hypotheses"]:
            del self._db[test_id]["Hypotheses"][hypothesis_id]

    def remove_agent(self, test_id, agent_id):
        if agent_id in self._db[test_id]["Agents"]:
            del self._db[test_id]["Agents"][agent_id]

    def remove_test(self, test_id):
        if test_id in self._db:
            del self._db[test_id]

    def get_all_agent_ids(self):
        return list(set([hypothesis_id for key in self._db for hypothesis_id in self._db[key]["Agents"]]))

    def get_all_hypothesis_ids(self):
        return list(set([hypothesis_id for key in self._db for hypothesis_id in self._db[key]["Hypotheses"]]))

    def get_all_test_ids(self):
        return [key for key in self._db]

    def get_test(self, test_id):
        return self._db[test_id] if test_id in self._db else None

    