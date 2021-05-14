
import numpy as np
import random

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface




class HypothesesLearning():        #This is the group method, as it should be. Should I use MongoDB? #Start making it without loading and saving. Results are handled by the inheritance. Should have Epsilon though
    _agentDB = None
    _hypothesisDB = None
    _testDB = None

    def __init__(self, model_addr):  #This is the agent and should therefore not hold an agent (I think, don't really know yet)
        self._model_addr = model_addr
        #self._create_directory(self._model_addr)
        self._create_dbs()

        agent_name = model_addr.split("/")[-1]
        self._agent_id = HypothesesLearning._agentDB.create(agent_name)


    def _create_dbs(self):
        if HypothesesLearning._agentDB == None:
            HypothesesLearning._agentDB = AgentDB()
        if HypothesesLearning._hypothesisDB == None:
            HypothesesLearning._hypothesisDB = HypothesisDB()
        if HypothesesLearning._testDB== None:
            HypothesesLearning._testDB = TestDB()

    
    def get_epsilon(self):
        return 0    #Should this be a factor that decide how much it is willing to experiment?









class Agent:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_info_str(self):
        return str(f"Name: {self._name}")





class Hypothesis:
    def __init__(self):
        pass




class Test:
    def __init__(self):
        self._hypothesis_ids = []

    def add_hypothesis(self, id):
        self._hypothesis_ids += [id]









class AgentDB:
    def __init__(self):
        self._db = {}

    def print_db(self):
        print("-------- Agent DB --------")
        for key in self._db:
            agent_id = self._db[key]["Id"]
            agent_info = self._db[key]["Agent"].get_info_str()
            hypotheses_ids = [key for key in self._db[key]["Hypotheses"]]
            print(f"Agent = Id: {agent_id}, info: {agent_info}")
            print(f"Hypotheses: {hypotheses_ids}")
            print("--")
        print("")

    def create(self, agent_name):
        rand_id = random.randint(0, 1000000000)
        while rand_id in self._db and self._db[rand_id].get_name() != agent_name:   #Create a new id if there already is a different agent with that id
            rand_id = random.randint(0, 1000000000)
        self._db[rand_id] = self._create_new_entry(rand_id, agent_name)
        return rand_id

    def _create_new_entry(sel, id, agent_name):
        return {"Id": id, "Agent": Agent(agent_name), "Hypotheses": {}}

    def add_hypothesis(self, agent_id, hypothesis_id):    #Hypothesis for now
        self._db[agent_id]["Hypotheses"][hypothesis_id] = {"Id": hypothesis_id}
    
    def remove_hypothesis(self, agent_id, hypothesis_id):
        del self._db[agent_id][hypothesis_id]

    def remove_agent(self, agent_id):
        del self._db[agent_id]





class HypothesisDB:
    def __init__(self):
        self._db = {}

    def create(self):
        rand_id = random.randint(0, 1000000000)
        while rand_id in self._db:
            rand_id = random.randint(0, 1000000000)
        self._db[rand_id] = self._create_new_entry(rand_id)
        return rand_id

    def _create_new_entry(self, id):
        return {"Id": id, "Hypothesis": Hypothesis(), "Tests": {}}




class TestDB:
    def __init__(self):
        self._db = {}

    def create(self):
        rand_id = random.randint(0, 1000000000)
        while rand_id in self._db:
            rand_id = random.randint(0, 1000000000)
        self._db[rand_id] = self._create_new_entry(rand_id)
        return rand_id

    def _create_new_entry(self, id):
        return {"Id": id, "Test": Test(), "Hypotheses": {}}