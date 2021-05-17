#------------------ Libraries -----------------
from Simulations.Environments import *
from BehaviouralModels.BehaviouralModels import *
from BehaviouralModels.GroupModels import *
from BehaviouralModels.HypothesisMethod.NewApproach import *
from GameSetupFiles import SetupFiles

#----------- Generate Game Features -----------
#project_features = SetupFiles.simple_group_features2()

#project_comb = [project_features[0], project_features[2], project_features[3]]

#-------------------- Main --------------------
#suite = EnvironmentSuit(len(project_comb), DeepReinforcementLearning, features=project_comb, verbose = 2, file_addr = "../Save/", sim_base_name="DQL_Group_1LCNN_2LDL_Simple_0_2_3", training=True)   
#suite.run(0)



model_0 = HypothesesLearning("model_0")
model_1 = HypothesesLearning("model_1")
model_2 = HypothesesLearning("model_2")

hypothesis_id_0 = HypothesesLearning._backend.create_hypothesis()
hypothesis_id_1 = HypothesesLearning._backend.create_hypothesis()
test_id_0 = HypothesesLearning._backend.create_test([0, 1, 2], [3, 4, 5], 3)    #More things can be added later
test_id_1 = HypothesesLearning._backend.create_test([0, [1]], [3, [4]], 1)    #But one of the things that could be added the change in score

HypothesesLearning._backend._agentDB.add_hypothesis(model_0._agent_id, hypothesis_id_0)
HypothesesLearning._backend._hypothesisDB.add_agent(hypothesis_id_0, model_0._agent_id)
HypothesesLearning._backend._hypothesisDB.add_test(hypothesis_id_0, test_id_1)

HypothesesLearning._backend.print_dbs()
print("###############################################")#
print("")


HypothesesLearning._backend.remove_hypothesis(hypothesis_id_0)

HypothesesLearning._backend.print_dbs()
print("###############################################")
print("")

print(HypothesesLearning._backend._agentDB.get_all_agent_ids())
print(HypothesesLearning._backend._hypothesisDB.get_all_hypothesis_ids())
print(HypothesesLearning._backend._testDB.get_all_test_ids())

diff = HypothesesLearning._backend._testDB.get_test(test_id_1)["Test"].get_difference()
print(diff.get_difference())

diff.remove_part(1)
print(diff.get_difference())

new_diff = HypothesesLearning._backend._testDB.get_test(test_id_0)["Test"].get_difference().get_diff_subset([0, 2])
print(new_diff.get_difference())

#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  

