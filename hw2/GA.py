# !/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *
from random import *
from math import exp
import logging
from pprint import pprint

error = 3
J = 3
p = 3
N = 20
selection = 'tournament' # choose 'roulette wheel' or 'tournament'
selecnum = 2 # only accept even number
crossoverprob = 0.5
mutationprob = 0.5

# read all file and store into dataset list
def getTrainData():
	dataset = list()
	for i in range(13):
		s = 'train_%d_D1.txt' %i
		f = open(s, 'r')
		for line in open(s):
			line = f.readline().splitlines()[0].split(' ')
			for i in range(4):
				line[i] = float(line[i])
			dataset.append(line)
		f.close()
	return dataset

# random produce initial Ethnicity
def initializeEthnicity():
	Ethnicity = list()
	for _ in range(N):
		Species = list()
		Species.append(random()) # theta = 0~1
		for _ in range(J):
			Species.append(uniform(-40, 40)) # wj = -40~40
		for _ in range(p*J):
			Species.append(uniform(0, 30)) # mj = 0~30
		for _ in range(J):
			Species.append(uniform(0, 10)) # phi j = 0~10
		Ethnicity.append(Species)
	return Ethnicity

# calculate adaptive value
def adaptiveFunction(dataset, Ethnicity):
	En = list() # store each Species' adaptiveFunction which associate with every data in dataset
	for Species in Ethnicity:
		En.append(0)
		for data in dataset:
			inputt = list(data[0:-1])
			output = data[-1]
			phi = list()
			for j in range(J):
				if Species[(1+J+p*J+j)] == 0:
					phi.append(0)
				else:
					#phi.append(exp(-sum((input - Species[(1+J+j*p): (1+J+j*p+p)])**2)/(2*Species[(1+J+p*J+j)]**2)))
					summ = 0
					for smallp in range(p):
						summ = summ + pow( (inputt[smallp] - Species[1+J+j*p+smallp]) , 2)
					summ = summ / (2 * (pow(Species[(1+J+p*J+j)], 2)))
					summ = summ * (-1)
					phi.append( exp(summ) )
			#phi = array(phi)
			#Fx = Species[0] + sum(Species[1: 1+J] * phi)
			Fx = Species[0]
			for i in range(1, 1+J):
				Fx = Fx + (Species[i] * phi[i-1])
			En[-1] = En[-1] + abs(output - Fx)
		En[-1] = En[-1] / len(dataset)
	return En

def stopOrNot(En, Ethnicity):
	minn = error # limit error
	minSpecies = -1 # store the Species who has the smallest adaptive value
	minSpecieserror = -1
	stop = False
	for i in range(len(Ethnicity)):
		if En[i] < minn:
			minSpecies = Ethnicity[i]
			minSpecieserror = En[i]
			stop = True
	print stop, minSpecieserror, minSpecies, min(En)
	return stop, minSpecieserror, minSpecies

# remove array in 2D array
def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not array_equal(L[ind],arr):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')

# reproduction
def reproduction(Ethnicity, En):
	newEthnicity = list()
	oldEthnicity = Ethnicity
	oldEn = En
	while True:
		if selection == 'tournament':
			chosennum = map(int, sample([str(i) for i in range(len(En))], 2))
			old1 = list([En[chosennum[0]], Ethnicity[chosennum[0]]])
			old2 = list([En[chosennum[1]], Ethnicity[chosennum[1]]])
			if old1[0] > old2[0]:
				old1, old2 = old2, old1
			newEthnicity.append(old1[1])
			newEthnicity.append(old1[1]) # copy twice into newEthnicity
			removearray(Ethnicity, old1[1])
			En.remove(old1[0])
			removearray(Ethnicity, old2[1])
			En.remove(old2[0])
			if(len(En) == 0):
				return oldEn, oldEthnicity, newEthnicity

# crossover
def crossover(Ethnicity):
	newEthnicity = list()
	while True:
		chosennum = map(int, sample([str(i) for i in range(len(Ethnicity))], 2))
		chosen = list()
		for index in chosennum:
			chosen.append(Ethnicity[index])
		removearray(Ethnicity, chosen[0])
		removearray(Ethnicity, chosen[1])
		#chosen = array(chosen)
		if random() < crossoverprob:
			sigma = uniform(-1, 1)
			'''new1 = chosen[0] + sigma * (chosen[0] - chosen[1])
			new2 = chosen[1] + sigma * (chosen[0] - chosen[1])'''
			new1 = list()
			new2 = list()
			for i in range(len(chosen[0])):
				new1.append( chosen[0][i] + sigma * (chosen[0][i] - chosen[1][i]) )
				new2.append( chosen[1][i] - sigma * (chosen[0][i] - chosen[1][i]) )
		else:
			new1 = chosen[0]
			new2 = chosen[1]
		#new1.tolist()
		#new2.tolist()
		newEthnicity.append(new1)
		newEthnicity.append(new2)
		if(len(Ethnicity) == 0):
			return newEthnicity

# mutation
def mutation(T, Ethnicity):
	newEthnicity = list()
	'''while True:
		chosenindex = randint(0, len(Ethnicity)-1)
		chosen = Ethnicity[chosenindex]
		del Ethnicity[chosenindex]
		if random() < mutationprob:
			s = exp(-T/500)
			for i in range(len(chosen)):
				if random() < 0.5:
					if i == 0: depend = 0.3
					elif i >= 1 and i <= J: depend = 24
					elif i >= J+1 and i <= J+p*J: depend = 9
					else: depend = 3
					chosen[i] += s * uniform(-1, 1) * depend
		newEthnicity.append(chosen)
		if(len(Ethnicity) == 0):
			return newEthnicity'''
	for Species in Ethnicity:
		if random() < mutationprob:
			s = exp(-T/500)
			for i in range(len(Species)):
				if random() < 0.5:
					if i == 0: depend = 0.3
					elif i >= 1 and i <= J: depend = 24
					elif i >= J+1 and i <= J+p*J: depend = 9
					else: depend = 3
					Species[i] = Species[i] + s*uniform(-1, 1) * depend
		newEthnicity.append(Species)
	return newEthnicity

# judge if satisfy the termination condition or not
def TerminationCondition(dataset, Ethnicity):
	T = 0 # store iteration #
	oldEn = list()
	while True:
		T = T + 1
		En = adaptiveFunction(dataset, Ethnicity)
		if oldEn:
			if min(oldEn) not in En:
				del Ethnicity[0]
				del En[0]
				Ethnicity.append(oldEthnicity[oldEn.index(min(oldEn))])
				En.append(oldEn[oldEn.index(min(oldEn))])
		stop, minSpecieserror, minSpecies = stopOrNot(En, Ethnicity)
		if stop:
			return T, minSpecies
		else:
			oldEn, oldEthnicity, Ethnicity = reproduction(Ethnicity, En)
			Ethnicity = crossover(Ethnicity)
			Ethnicity = mutation(T, Ethnicity)
			# limit values in Ethnicity
			for Species in Ethnicity:
				if Species[0] > 1: Species[0] = 1 
				elif Species[0] < 0: Species[0] = 0
				for i in range(1, 1+J):
					if Species[i] > 40: Species[i] = 40 
					elif Species[i] < -40: Species[i] = -40
				for i in range(1+J, 1+J+p*J):
					if Species[i] > 30: Species[i] = 30 
					elif Species[i] < 0: Species[i] = 0
				for i in range(1+J+p*J, 1+J+p*J+J):
					if Species[i] > 10: Species[i] = 10 
					elif Species[i] < 0: Species[i] = 0


dataset = getTrainData()
Ethnicity = initializeEthnicity()
iterationnum, bestsolution = TerminationCondition(dataset, Ethnicity)
print 'iterationnum: ', iterationnum
print 'bestsolution: ', bestsolution
f = open('bestsolution.txt', 'w')
for item in bestsolution:
	f.write("%s,\t" % item)
