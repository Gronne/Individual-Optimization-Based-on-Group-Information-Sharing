#------------------ Libraries -----------------
from Simulations.Environments import *
from BehaviouralModels.BehaviouralModels import *
from BehaviouralModels.IndividualModels import *
from BehaviouralModels.HypothesisMethod.NewApproach import *
from GameSetupFiles import SetupFiles

#----------- Generate Game Features -----------
project_features = SetupFiles.simple_group_features()

#-------------------- Main --------------------
suite = EnvironmentSuit(len(project_features), QLearning, features=project_features, verbose = 2, file_addr = "../Save/", sim_base_name="Test_QLearning", training=True)   
suite.run(0)


