#------------------ Libraries -----------------
from Simulations.Environments import *
from BehaviouralModels.BehaviouralModels import *
from BehaviouralModels.IndividualModels import *
from GameSetupFiles import SetupFiles

#----------- Generate Game Features -----------
project_features = SetupFiles.simple_features2()

#-------------------- Main --------------------
suite = EnvironmentSuit(len(project_features), DeepReinforcementLearning, features=project_features, verbose = 2, file_addr = "../Save/", sim_base_name="DQL_Indi_Test_v9", training=True)   
suite.run(0)

#Make a simple_features but for the group training. This one have the other simple game but also a second one the only have one dot
#The goal is to confuser one of them as it will belive that more positive reward is in corner.