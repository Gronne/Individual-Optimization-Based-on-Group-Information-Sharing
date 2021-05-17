
import numpy as np
from collections import deque

from Simulations.GameFeatures import GameFeatures as GF
from BehaviouralModels.BehaviouralModels import BehaviouralModelInterface
from BehaviouralModels.HypothesisMethod.HypothesisDBStructures import *
from BehaviouralModels.HypothesisMethod.HypothesisConceptStructures import *
from BehaviouralModels.HypothesisMethod.HypothesisBackend import *





class HypothesesLearning():        #This is the group method, as it should be. Should I use MongoDB? #Start making it without loading and saving. Results are handled by the inheritance. Should have Epsilon though
    _backend = None

    def __init__(self, model_addr):  #This is the agent and should therefore not hold an agent (I think, don't really know yet)
        self._model_addr = model_addr
        #self._create_directory(self._model_addr)
        self._create_backend()
        self._feasible_actions = [0, 1, 2, 3, 4]

        agent_name = model_addr.split("/")[-1]
        self._agent_id = HypothesesLearning._backend.create_agent(agent_name)

        self._replay_memory = deque()


    def _create_backend(self):
        if HypothesesLearning._backend == None:
            HypothesesLearning._backend = HypothesisBackend()
    
    def get_epsilon(self):
        return 0    #Should this be a factor that decide how much it is willing to experiment?

    def _get_tests(self):
        return HypothesesLearning._backend.get_agent_tests(self._agent_id)

    def _get_hypotheses(self):
        return HypothesesLearning._backend.get_agent_hypotheses(self._agent_id)

    def _update_replay_memory(self, transition):
        self._replay_memory.append(transition)

    def action(self, game_state, training = True):
        model_state = self._game_to_model_state(game_state)
        action = self._train(model_state) if training else self._optimal_action(model_state)
        return action

    def _game_to_model_state(self, game_state): #The model state will always be dependent on what is required for the model
        #[Steps, Life, Points, Coordinates, game_state]
        return [0, 1, 2, 3, 4]

    def _train(self, current_state):
        current_score = BehaviouralModelInterface._calculate_score(current_state[0], current_state[2], current_state[3])
        trigger = self._trigger(current_state, current_score)
        
        if trigger["Name"] == "score change":
            pass
        elif trigger["Name"] == "hypothesis":
            pass
        else:
            pass #No trigger -> Discovery -> Random Action

        if self._first_action():
            #Check if test or discovery, check for hypotheses in the DB
            hypotheses = self._backend.get_test_worthy_hypotheses(current_state)
            hypothesis = self._choose_hypothesis(hypotheses)

        #First action in state
        if not len(self._replay_memory):
            random_action = np.random.randint(0, len(self._feasible_actions))
            self._update_replay_memory([None, current_state, None, current_score, random_action])   #What about death?
            #It should just take a random action, this should only be done when it is the first ever action.
            #It should check if there is anuthing to test or discover in the DB.
            return random_action

        _, previous_state, _, previous_score, previous_action = self._replay_memory[-1]
        
        #Change in score will trigger a hypothesis
        #Maybe I should just start by adding hypothesis and do the rest later. You know, one step at the time

        #If not trigger, check if anything can lead to a


        #First an action then 

        state_difference = self.state_diff(current_state, previous_state)


        action = None
        self._update_replay_memory([previous_state, current_state, previous_action, current_score, action])
        return action

    def _trigger(self, current_state, score):
        pass

    def _first_action(self):
        return len(self._replay_memory) == 0

    def _choose_hypothesis(self, hypothesis):
        pass

    def state_diff(current_state, previous_state):
        pass


    def _optimal_action(self, model_state):
        #This is probably going to be the part where optimization is happening or at least used. 
        #The training/discovery phase is soly to set the system up for optimization
        return 0










