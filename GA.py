# Genetic algorithm for printing "Hello World!"

import random
import math

# Initialize
def Initialize(populationSize, nLetters):
	
	nucleotides = [chr(i) for i in range(128)]
	#nucleotides = ['H','e','l','o',' ','W','r','d','!']
	population = []
	random.seed()
	
	for i in range(0, populationSize):
		population.append([])
		for j in range(0, nLetters):
			r = random.randint(0, len(nucleotides)-1)
			population[i].append(nucleotides[r])
		
	return (population, nucleotides)
	
# CalculateFitness
def CalculateFitness(message, population):
	
	fitness = []
	
	for i in range(len(population)):
		fitness.append(0)
		for j in range(len(message)):
			if population[i][j] == message[j]:
				fitness[i] = fitness[i] + 1
	
	return fitness

# CheckFitness
def CheckFitness(fitness, nLetters):
	
	fit = False 
	fitIndex = 0
	
	for i in range(len(fitness)):
		if fitness[i] == nLetters:
			fit = True
			fitIndex = i
			
	return fit, fitIndex
	
# CullTheHerd
def CullTheHerd(population, fitness):
	
	for i in range(len(population)-1,-1,-1): # loop backwards so as not to disturb indices during deletion
		if fitness[i] == 0:
			del population[i]
			del fitness[i]
		
	return (population, fitness)
	
# Sort by fitness
def SortByFitness(population, fitness):
	listOfTuplesToSort = list(zip(fitness,population))
	sortedListOfTuples = sorted(listOfTuplesToSort, reverse=True)
	ListOfListsByTupleIndex = list(zip(*sortedListOfTuples))
	fitness = ListOfListsByTupleIndex[0]
	population = ListOfListsByTupleIndex[1]
	return population, fitness
	
# Helper functions for Crossover
# =========================================================================================================
# FirstHalf
def FirstHalf(fullList):
	length = len(fullList)
	half = round(length/2)
	firstHalf = fullList[0:half]
	return firstHalf
	
# SecondHalf
def SecondHalf(fullList):
	length = len(fullList)
	half = round(length/2)
	secondHalf = fullList[half:length]
	return secondHalf
# =========================================================================================================
	
# Crossover
def Crossover(population,populationSize):
	
	nextGeneration = []
	
	# Keep 10 best from last generation
	for i in range(10):
		nextGeneration.append(population[i])
	
	for i in range(math.floor(math.sqrt(len(population)))):# 10 intead of len(population) to limit size
		firstHalf = FirstHalf(population[i])
		for j in range(math.floor(math.sqrt(len(population)))):# 10 instead of len(population) to limit size
			if i != j: # don't cross over with self
				secondHalf = SecondHalf(population[j])
				nextGeneration.append(firstHalf + secondHalf)
	
	#return nextGeneration[0:populationSize] # truncate
	return nextGeneration

# Mutate
def Mutate(population, nucleotides):
	
	# we want about one mutation per member of population
	mutationRate = 1.0/len(population[0]);
	random.seed()
	
	for i in range(len(population)):
		for j in range(len(population[0])):
			if random.random() < mutationRate:
				charIndex = random.randint(0,len(nucleotides)-1)
				population[i][j] = nucleotides[charIndex]
	
	return population
	
# Reproduce
def Reproduce(population, populationSize, nucleotides):
	
	# Crossover
	nextGeneration = Crossover(population, populationSize)
	# Mutate
	nextGeneration = Mutate(nextGeneration, nucleotides)
	
	return nextGeneration
	
# MakeString
def MakeString(charList):
	return ''.join(charList)

def main():

	print("\nWhat string would you like to build?\n")
	message = input("String: ")

	populationSize = 500
	genCount = 0
	nLetters = len(message)
	(population, nucleotides) = Initialize(populationSize, nLetters)

	while(True):
		genCount = genCount + 1
		fitness = CalculateFitness(message, population)
		(population, fitness) = CullTheHerd(population, fitness)
		(population, fitness) = SortByFitness(population, fitness)
		population = population[0:populationSize] # truncate
		
		# print statistics
		fittest = MakeString(population[0])
		leastFit = MakeString(population[len(population)-1])
		print("\nGeneration: ", genCount,"\nFittest  : ", fittest, "\nFitness: ", fitness[0])
		
		if fitness[0] == nLetters:
			print("\n")
			break
			
		population = Reproduce(population, populationSize, nucleotides)
		
	helloWorld = population[0]
	helloWorldString = MakeString(helloWorld)
	#print(helloWorldString)


if __name__ == "__main__":
    # execute only if run as a script
    main()