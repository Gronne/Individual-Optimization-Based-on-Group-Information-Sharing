#------------------ Libraries -----------------
from Simulations.Environments import *
from BehaviouralModels.BehaviouralModels import *
from BehaviouralModels.IndividualModels import *
from GameSetupFiles import SetupFiles

#----------- Generate Game Features -----------
project_features = SetupFiles.project_features()[:2]

#-------------------- Main --------------------
suite = EnvironmentSuit(len(project_features), QLearning, features=project_features, verbose = 2)   
suite.run(512)
