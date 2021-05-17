import os
import numpy as np
import matplotlib.pyplot as plt




class VisualiseModelData:
    def plot_score(addresses, names, title="Performance", nr_of_deaths = 10, different_diagrams = True):
        for count, address in enumerate(addresses):
            deaths = [count for count in range(0, nr_of_deaths)]
            epsilon, score, point, survival_time = VisualiseModelData._load_result_data(address, nr_of_deaths, False)
            figure = plt.figure()
            axes = figure.add_subplot(111)  #The Y-axis should be between 0 and 100
            axes.set_xlabel('Deaths')
            axes.set_title(title + " for " + names[count])

            axes.plot(deaths, epsilon, color="tab:blue")
            axes.plot(deaths, score, color="tab:red")
            axes.plot(deaths, point, color="tab:green")
            axes.plot(deaths, survival_time, color="tab:orange")

    def _load_result_data(address, nr_of_deaths=10, training_flag=False):
        epsilons = []
        scores = []
        points = []
        survival_times = []
        with open(address + ".txt") as model_file:
            for line_count, line in enumerate(model_file):
                if line_count >= nr_of_deaths:
                    break
                survival_time, point, epsilon, training = line.split(",")
                if training_flag == (True if training.split(':')[1] == "True" else False):
                    epsilons += [(1-float(epsilon.split(':')[1]))*100]
                    scores += [float(point.split(':')[1])]
                    points += [int(point.split(':')[1])]
                    survival_times += [int(survival_time.split(':')[1])/10]
        return epsilons, scores, points, survival_times


    def plot_memory(addresses, names, title = "Memory"):
        sizes = [os.path.getsize(address+".txt")/(1000*1000) for address in addresses]
        figure = plt.figure()
        axes = figure.add_subplot(111)
        axes.bar(names, sizes)
        axes.set_ylabel('Memory size (MB)')
        axes.set_xlabel('Models')
        axes.set_title(title)



addresses_memory = ["../Save/QL_Indi_All/models/model_0", "../Save/QL_Indi_All/models/model_1", "../Save/QL_Indi_All/models/model_2"]
addresses_score = ["../Save/QL_Indi_All/results/result_0", "../Save/QL_Indi_All/results/result_1", "../Save/QL_Indi_All/results/result_2"]
names = ["model 0", "model 1", "model 2"]



VisualiseModelData.plot_memory(addresses_memory, names, "QL Individual Memory")
VisualiseModelData.plot_score(addresses_score, names, "QL Individual Performance", nr_of_deaths=50)
plt.show()