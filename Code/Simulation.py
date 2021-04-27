#------------------ Libraries -----------------
from Simulations.Environments import *
from BehaviouralModels.BehaviouralModels import *
from BehaviouralModels.IndividualModels import *
from GameSetupFiles import SetupFiles

#----------- Generate Game Features -----------
project_features = [SetupFiles.project_features()[1]]

#-------------------- Main --------------------
suite = EnvironmentSuit(len(project_features), QLearning, features=project_features, verbose = 2, file_addr = "../Save/", sim_base_name="QL_Indi_V2")   
suite.run(0)
