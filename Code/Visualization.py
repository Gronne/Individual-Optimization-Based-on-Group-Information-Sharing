import os
import numpy as np
import matplotlib.pyplot as plt




class VisualiseModelData:
    def plot_score_different(addresses, names, title="Performance", nr_of_deaths = 10, different_diagrams = True, survival=False):
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
            if survival: axes.plot(deaths, survival_time, color="tab:orange")

    def plot_score_same(addresses, names, title="Performance", nr_of_deaths = 10, different_diagrams = True, survival=False):
        figure = plt.figure()
        colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]
        for count, address in enumerate(addresses):
            deaths = [count for count in range(0, nr_of_deaths)]
            epsilon, score, point, survival_time = VisualiseModelData._load_result_data(address, nr_of_deaths, False)
            
            axes = figure.add_subplot(111)  #The Y-axis should be between 0 and 100
            axes.set_xlabel('Deaths')
            axes.set_title(title + " for " + names[count])

            axes.plot(deaths, score, color="tab:" + colors[count])
            axes.plot(deaths, point, color="tab:" + colors[count])
            if survival: axes.plot(deaths, survival_time, color="tab:orange")

    def score_print(addresses, names, nr_of_deaths = 10, training_flag = False):
        for count, address in enumerate(addresses):
            deaths = [count for count in range(0, nr_of_deaths)]
            epsilon, score, point, survival_time = VisualiseModelData._load_result_data(address, nr_of_deaths, training_flag)
            print("".join(str(p)+", " for p in point))

    def _load_result_data(address, nr_of_deaths=10, training_flag=False):
        epsilons = []
        scores = []
        points = []
        survival_times = []
        line_count = 0
        with open(address + ".txt") as model_file:
            for line in model_file:
                if line_count >= nr_of_deaths:
                    break
                survival_time, point, epsilon, training = line.split(",")
                if training_flag == (True if training.split(':')[1][:-1] == "True" else False):
                    epsilons += [(1-float(epsilon.split(':')[1]))*100]
                    scores += [float(point.split(':')[1])]
                    points += [int(point.split(':')[1])]
                    survival_times += [int(survival_time.split(':')[1])/10]
                    line_count += 1
        return epsilons, scores, points, survival_times


    def plot_memory(addresses, names, title = "Memory"):
        sizes = [os.path.getsize(address+".txt")/(1000*1000) for address in addresses]
        figure = plt.figure()
        axes = figure.add_subplot(111)
        axes.bar(names, sizes)
        axes.set_ylabel('Memory size (MB)')
        axes.set_xlabel('Models')
        axes.set_title(title)

    def bar_diagram(sizes, names, title = "Memory"):
        font_title = {'size'   : 16}
        font_axes = {'size'   : 12}
        figure = plt.figure()
        axes = figure.add_subplot(111)
        axes.bar(names, sizes)
        axes.set_ylabel('Memory size (MB)', **font_axes)
        axes.set_xlabel('Models', **font_axes)
        axes.set_title(title, **font_title)


    def memory_graphs():
        SIA_QL = (0.664 + 0.336 + 0.598 + 0.598)/4
        SIA_RQL = (0.0123 + 0.0123 + 0.0123 + 0.0123)/4
        SIA_DQL = (28.1 + 28.1 + 28.1 + 28.1)/4
        SIA_HL = 10

        SGA_QL = (0.598 + 0.336 + 0.598 + 0.598 + 0.729 + 2.1 + 0.598 + 0.860 + 0.664 + 2.1 + 2.1 + 0.729 + 2.1 + 2.1 + 2.1)/1
        SGA_RQL = (0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123 + 0.0123)/15
        SGA_DQL = (28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1 + 28.1)/15
        SGA_HL = 14

        CIA_QL = (3274 + 929 + 3288 + 1288 + 2236 + 2223 + 65)/7
        CIA_RQL = (0.0833 + 0.0833 + 0.0833 + 0.0833 + 0.0833 + 0.0833 + 0.0833)/7
        CIA_DQL = (41.7 + 41.7 + 41.7 + 41.7 + 41.7 + 41.7 + 41.7)/7
        CIA_HL = 100

        CGA_QL = (2870 + 2970 + 4460 + 3790)/4
        CGA_RQL = (0.0833 + 0.0833 + 0.0833 + 0.0833)/4
        CGA_DQL = (41.7 + 41.7 + 41.7 + 41.7)/4
        CGA_HL = 150

        VisualiseModelData.bar_diagram([SIA_QL, SIA_RQL, SIA_DQL, SIA_HL], ["QL", "RQL", "DQL", "HL"], "Simple Individual Average Memory")
        VisualiseModelData.bar_diagram([SGA_QL, SGA_RQL, SGA_DQL, SGA_HL], ["QL", "RQL", "DQL", "HL"], "Simple Group Average Memory")
        VisualiseModelData.bar_diagram([CIA_QL, CIA_RQL, CIA_DQL, CIA_HL], ["QL", "RQL", "DQL", "HL"], "Complex Individual Average Memory")
        VisualiseModelData.bar_diagram([CGA_QL, CGA_RQL, CGA_DQL, CGA_HL], ["QL", "RQL", "DQL", "HL"], "Complex Group Average Memory")



addresses_memory = ["../Save/QL_Indi_All/models/model_0", "../Save/QL_Indi_All/models/model_1", "../Save/QL_Indi_All/models/model_2"]

addresses_score = [ "../Results/QLearning/QL_Group_Simple_0_2_V3/result_0",
                    "../Results/QLearning/QL_Group_Simple_0_2_V3/result_1", ]

names = [ "S0", "S1", "S2", "S3", "S4", "S5", "S0&1", "S0&2", "S0&5", "S0&3&4", "S0", "S1", "S2", "S3", "S4", "S5", "S0&1", "S0&2", "S0&5", "S0&3&4" ]



#VisualiseModelData.plot_memory(addresses_memory, names, "QL Individual Memory")
#VisualiseModelData.plot_score_same(addresses_score, names, "QL Individual Performance", nr_of_deaths=50)

#VisualiseModelData.score_print(addresses_score, names, nr_of_deaths=50, training_flag=False)
VisualiseModelData.score_print(addresses_score, names, nr_of_deaths=100, training_flag=True)
VisualiseModelData.score_print(addresses_score, names, nr_of_deaths=100, training_flag=False)


plt.show()