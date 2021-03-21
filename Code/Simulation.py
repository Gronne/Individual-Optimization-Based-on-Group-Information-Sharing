from Environments import *
from BehaviouralModels import *
from GameFeatures import GameFeatures as GF
from GameSetupFiles import SetupFiles


#----------- Generate Game Features -----------
first_features = SetupFiles.project_features()

#-------------------- Main --------------------
suite = EnvironmentSuit(len(first_features), BehaviouralModelInterface, features=first_features, verbose = 2)
suite.run(512)

