# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level = logging.DEBUG)
from pprint import pprint
from random import *
from math import exp

error = 3.95
J = 3
p = 5
N = 10
w = 0.7
alpha = 1.5
beta = 1.5

# read all file and store into dataset list
def getTrainData():
	dataset = list()
	for i in range(13):
		s = 'train_%d_D2.txt' %i
		f = open(s, 'r')
		for line in open(s):
			line = f.readline().splitlines()[0].split(' ')
			for i in range(len(line)):
				line[i] = float(line[i])
			dataset.append(line)
		f.close()
	return dataset

# random produce initial Swarm
def initializeSwarm():
	Swarmx = list()
	Swarmv = list()
	pbest = list() # none list when first initialize
	gbest = list() # none list when first initialize 
	adaptp = list() # error 100 when first initialize 
	adaptg = 100 # error 100 when first initialize 
	for _ in range(N):
		x = list()
		v = list()
		x.append(random()) # theta = 0~1
		v.append(0.01 * random())
		pbest.append([])
		adaptp.append(100)
		for _ in range(J):
			x.append(uniform(-40, 40)) # wj = -40~40
			v.append(0.01 * uniform(-40, 40))
		for _ in range(p*J):
			x.append(uniform(0, 30)) # mj = 0~30
			v.append(0.01 * uniform(0, 30))
		for _ in range(J):
			x.append(uniform(0, 10)) # phi j = 0~10
			v.append(0.01 * uniform(0, 10))
		Swarmx.append(x)
		Swarmv.append(v)
	return Swarmx, Swarmv, pbest, gbest, adaptp, adaptg

# calculate adaptive value
def adaptiveFunction(dataset, Swarmx):
	En = list() # store each Particle' adaptiveFunction which associate with every data in dataset
	for Particle in Swarmx:
		En.append(0)
		for data in dataset:
			inputt = list(data[0:-1])
			output = data[-1]
			phi = list()
			for j in range(J):
				if Particle[(1+J+p*J+j)] == 0:
					phi.append(0)
				else:
					summ = 0
					for smallp in range(p):
						summ = summ + pow( (inputt[smallp] - Particle[1+J+j*p+smallp]) , 2)
					summ = summ / (2 * (pow(Particle[(1+J+p*J+j)], 2)))
					summ = summ * (-1)
					phi.append( exp(summ) )
			Fx = Particle[0]
			for i in range(1, 1+J):
				Fx = Fx + (Particle[i] * phi[i-1])
			En[-1] = En[-1] + abs(output - Fx)
		En[-1] = En[-1] / len(dataset)
	return En

def stopOrNot(T, En, Swarmx):
	minn = error # limit error
	minParticle = -1 # store the Particle who has the smallest adaptive value
	minerror = -1
	stop = False
	for i in range(len(Swarmx)):
		if En[i] < minn:
			minParticle = Swarmx[i]
			minerror = En[i]
			stop = True
	print T, stop, minerror, minParticle, min(En)
	return stop, minerror, minParticle

def FindPbest(Swarmx, En, pbest, adaptp):
	for i in range(len(En)):
		if En[i] < adaptp[i]:
			adaptp[i] = En[i]
			pbest[i] = Swarmx[i]
	return pbest, adaptp

def FindGbest(Swarmx, En, gbest, adaptg):
	adaptg = 100
	for i in range(len(En)):
		if En[i] < adaptg:
			adaptg = En[i]
			gbest = Swarmx[i]
	return gbest, adaptg

def Fly(T, Swarmx, Swarmv, pbest, gbest):
	s = 0.05 * exp(-T/2000)
	for i in range(len(Swarmx)):
		for d in range(len(Swarmx[0])):
			Swarmv[i][d] = w * Swarmv[i][d] + random() * alpha * (pbest[i][d] - Swarmx[i][d]) + random() * beta * (gbest[d] - Swarmx[i][d])
			# limit vmax and vmin
			if d == 0:
				if Swarmv[i][d] > 1 * s: Swarmv[i][d] = 1 * s
				elif Swarmv[i][d] < -1 * s: Swarmv[i][d] = -1 * s
			if d >= 1 and d <= J:
				if Swarmv[i][d] > 80 * s: Swarmv[i][d] = 80 * s
				elif Swarmv[i][d] < -80 * s: Swarmv[i][d] = -80 * s
			if d >= J+1 and d <= J+p*J:
				if Swarmv[i][d] > 30 * s: Swarmv[i][d] = 30 * s
				elif Swarmv[i][d] < -30 * s: Swarmv[i][d] = -30 * s
			if d >= 1+J+p*J and d <= J+p*J+J:
				if Swarmv[i][d] > 10 * s: Swarmv[i][d] = 10 * s
				elif Swarmv[i][d] < -10 * s: Swarmv[i][d] = -10 * s
			
			Swarmx[i][d] = Swarmx[i][d] + Swarmv[i][d]
	return Swarmx, Swarmv
# judge if satisfy the termination condition or not
def TerminationCondition(dataset, Swarmx, Swarmv, pbest, gbest, adaptp, adaptg):
	T = 0 # store iteration
	while True:
		T = T + 1
		En = adaptiveFunction(dataset, Swarmx)
		stop, minerror, minParticle = stopOrNot(T, En, Swarmx)
		if stop:
			return T, minerror, minParticle
		else:
			pbest, adaptp = FindPbest(Swarmx, En, pbest, adaptp)
			gbest, adaptg = FindGbest(Swarmx, En, gbest, adaptg)
			Swarmx, Swarmv = Fly(T, Swarmx, Swarmv, pbest, gbest)
			# limit values in Swarmx
			for Particle in Swarmx:
				if Particle[0] > 1: Particle[0] = 1 
				elif Particle[0] < 0: Particle[0] = 0
				for i in range(1, 1+J):
					if Particle[i] > 40: Particle[i] = 40 
					elif Particle[i] < -40: Particle[i] = -40
				for i in range(1+J, 1+J+p*J):
					if Particle[i] > 30: Particle[i] = 30 
					elif Particle[i] < 0: Particle[i] = 0
				for i in range(1+J+p*J, 1+J+p*J+J):
					if Particle[i] > 10: Particle[i] = 10 
					elif Particle[i] < 0: Particle[i] = 0

dataset = getTrainData()
Swarmx, Swarmv, pbest, gbest, adaptp, adaptg = initializeSwarm()
iterationnum, besterror, bestsolution = TerminationCondition(dataset, Swarmx, Swarmv, pbest, gbest, adaptp, adaptg)

print 'iterationnum: ', iterationnum
print 'besterror:', besterror
print 'bestsolution: ', bestsolution
