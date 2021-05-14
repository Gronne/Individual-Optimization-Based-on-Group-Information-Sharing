#------------------ Libraries -----------------
from Simulations.Environments import *
from BehaviouralModels.BehaviouralModels import *
from BehaviouralModels.IndividualModels import *
from BehaviouralModels.NewApproach import *
from GameSetupFiles import SetupFiles

#----------- Generate Game Features -----------
#project_features = SetupFiles.project_features()

#-------------------- Main --------------------
#suite = EnvironmentSuit(len(project_features), DeepReinforcementLearning, features=project_features, verbose = 2, file_addr = "../Save/", sim_base_name="DQL_Indi_All_V1_1L_CNN_2L_DL", training=True)   
#suite.run(0)




model_0 = HypothesesLearning("model_0")
model_1 = HypothesesLearning("model_1")
model_2 = HypothesesLearning("model_2")

HypothesesLearning._agentDB.print_db()

hypo_0_id = HypothesesLearning._hypothesisDB.create()
HypothesesLearning._agentDB.add_hypothesis(model_0._agent_id, hypo_0_id)

HypothesesLearning._agentDB.print_db()
