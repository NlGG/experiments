import numpy as np
import matplotlib.pyplot as plt

class AnalysisCI():
	def __init__(self, datalist, networktype):
		self.network_data_np = datalist
		self.networktype = networktype

	def calculate(self):

		total= [[],[],[],[],[]]

		networktype = self.networktype
		network_data_np = self.network_data_np

		for i in range(len(network_data_np)):
		    if network_data_np[i][1] == networktype:
		        if network_data_np[i][2] == 'A':
		            if network_data_np[i][3] == 'ACTIVE':
		                total[0].append([1])
		            else:
		                total[0].append([0])
		        if network_data_np[i][2] == 'B':
		            if network_data_np[i][3] == 'ACTIVE':
		                total[1].append([1])
		            else:
		                total[1].append([0])
		        if network_data_np[i][2] == 'C':
		            if network_data_np[i][3] == 'ACTIVE':
		                total[2].append([1])
		            else:
		                total[2].append([0])
		        if network_data_np[i][2] == 'D':
		            if network_data_np[i][3] == 'ACTIVE':
		                total[3].append([1])
		            else:
		                total[3].append([0])
		        if network_data_np[i][2] == 'E':
		            if network_data_np[i][3] == 'ACTIVE':
		                total[4].append([1])
		            else:
		                total[4].append([0])
		return total

	def show(self, role):
		if role == 'A':
			num = 0
		elif role == 'B':
			num = 1
		elif role == 'C':
			num = 2
		elif role == 'D':
			num = 3
		else:
			num = 4

		total = self.calculate()

		plt.plot(total[num], "o") 
		plt.title(role)
		plt.show()

class AnalysisII():
	def __init__(self, datalist):
		self.network_data_np = datalist

	def calculate(self):
		network_data_np = self.network_data_np
		total_1 = [0.0 for i in range(40)]
		total_2 = [0.0 for i in range(40)]
		total_3 = [0.0 for i in range(40)]

		total_1_active = [0.0 for i in range(40)]
		total_2_active = [0.0 for i in range(40)]
		total_3_active = [0.0 for i in range(40)]

		total_1_per  = [0.0 for i in range(40)]
		total_2_per  = [0.0 for i in range(40)]
		total_3_per  = [0.0 for i in range(40)]

		for i in range(len(network_data_np)):
		    num_round = network_data_np[i][0]
		    if network_data_np[i][3] == 'INACTIVE':
		        network_data_np[i][6] = 50.0
		    if network_data_np[i][4] == 1:
		        total_1[num_round-1] += 1.0
		        if network_data_np[i][3] == 'ACTIVE':
		            total_1_active[num_round-1] += 1.0
		            total_1_per[num_round-1] = total_1_active[num_round-1] / total_1[num_round-1]
		    elif network_data_np[i][4] == 2:
		        total_2[network_data_np[i][0]-1] += 1.0
		        if network_data_np[i][3] == 'ACTIVE':
		            total_2_active[num_round-1] += 1.0
		            total_2_per[num_round-1] = total_2_active[num_round-1] / total_2[num_round-1]
		    else:
		        total_3[network_data_np[i][0]-1] +=1.0
		        if network_data_np[i][3] == 'ACTIVE':
		            total_3_active[num_round-1] += 1.0
		            total_3_per[num_round-1] = total_3_active[num_round-1] / total_3[num_round-1]

		total = [total_1_per, total_2_per, total_3_per]
		return  total

	def show1(self):
		total = self.calculate()
		plt.plot(total[0], "o") 
		plt.title("1")
		plt.show()

	def show2(self):
		total = self.calculate()
		plt.plot(total[1], "o") 
		plt.title("2")
		plt.show()

	def show3(self):
		total = self.calculate()
		plt.plot(total[2], "o") 
		plt.title("3")
		plt.show()

