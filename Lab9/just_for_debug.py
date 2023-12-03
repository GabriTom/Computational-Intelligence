import random
import lab9_lib
import copy
import numpy as np
from random import choices

PROBLEM_SIZES = [1, 2, 5, 10]
FITNESS_THRESHOLD = 0.9
LOCI = 1000
STAGNATION = 100

class LocalSearch:
    def __init__(self, mut_rate, cmb_rate, blck_size, prb_size):
        self.mutation_rate = mut_rate
        self.combination_rate = cmb_rate
        #Block size expressed in percentage
        self.block_size = blck_size
        self.best_fit = -1
        #Size retrieved in survival selection phase
        self.problem_size = prb_size
        self.fitness = lab9_lib.make_problem(prb_size)
        self.population = []

    #Function that generates a population of n_individuals and sort them w.r.t. the fitness function
    def generate_population(self, n_individuals):
        for _ in range(n_individuals):
            ind = choices([0, 1], k=LOCI)
            self.population.append(ind)
        self.population.sort(reverse=True, key=self.fitness)
        self.best_fit = self.fitness(self.population[0])

    #Function that receives a genome ad return a mutated version of it accordingly to a random choice 
    #and a mutation paremeter, that can change.
    #Changes are given by the best_fit. If after a mutation best_fit increases that mutation will
    #be applied with more probability.
    def mutate(self, genome):
        mutated_genome = []
        for _ in genome:
            if random.random() <= self.mutation_rate:
                mutated_genome.append(1)
            else:
                mutated_genome.append(0)
        return mutated_genome

    #Function that receives two genomes and returns a combined version of the two.
    #The combination happens at a very specific level. In fact each element (bit from 
    # our poit of view) of the genome is taken into consideration before swapping.
    # def combine_genomes_bit_level(self, gen_1, gen_2):
    #     combined_1 = []
    #     combined_2 = []

    #     for i in range(len(gen_1)):
    #         if random.random() > self.combination_rate:
    #             tmp = gen_1[i]
    #             gen_1[i] = gen_2[i]
    #             gen_2[i] = tmp

    #     return combined_1, combined_2

    #Function that receives two genomes and returns a combined version of the two.
    #The combination happens at block level.
    def combine_genomes_block_level(self, gen_1, gen_2):
        combined_1 = copy.deepcopy(gen_1)
        combined_2 = copy.deepcopy(gen_2)
        bound = self.block_size
        start = 0

        for _ in range(int(len(gen_1)/self.block_size)):
            if random.random() > self.combination_rate:
                tmp = combined_1[start:bound]
                combined_1[start:start+self.block_size] = combined_2[start:start+self.block_size]
                combined_2[start:start+self.block_size] = tmp
            start += self.block_size

        return combined_1, combined_2
    
    #Function that extracts two parents among the population. It can be the same individual twice.
    def parent_selection(self):
        p_1 = self.population[random.randint(0, len(self.population)-1)]
        p_2 = self.population[random.randint(0, len(self.population)-1)]
        return p_1, p_2

    #Function that replaces the less fit individual with the current one.
    def survival_selection(self, ind):
        self.population[-1] = (copy.deepcopy(ind))
        self.population.sort(reverse=True, key=self.fitness)
        self.best_fit = self.fitness(self.population[0])

if __name__ == "__main__":
    #Variables that helps for stagnation
    cnt = 0
    best_prev = 0

    #Solving problem for given instances
    for problem_size in PROBLEM_SIZES:
        ls = LocalSearch(0.9, 0.5, 5, problem_size)
        ls.generate_population(problem_size)

        while ls.best_fit < FITNESS_THRESHOLD:
            #Only mutating if I have one individual
            if len(ls.population) == 1:
                ind = ls.population[random.randint(0, len(ls.population)-1)]
                ind_mut = ls.mutate(ind)
                if ls.fitness(ind_mut) > ls.best_fit:
                    #Changing mutation rate accordingly to the modify that just happened.
                    if np.sum(ind_mut) > np.sum(ind):
                        ls.mutation_rate *= 1.1
                    else:
                        ls.mutation_rate *= 0.9
                    ls.survival_selection(ind_mut)
            #Mutating and recombinig if I have more individuals
            else:
                ind_1, ind_2 = ls.parent_selection()
                cmb_1, cmb_2 = ls.combine_genomes_block_level(ind_1, ind_2)

                #Mutating if combining leads to stagnation
                if best_prev == ls.best_fit:
                    cnt += 1
                else:
                    best_prev = ls.best_fit
                    cnt = 0
                if cnt > STAGNATION:
                    cmb_1 = ls.mutate(cmb_1)
                    cmb_2 = ls.mutate(cmb_2)
                
                if ls.fitness(cmb_1) > ls.best_fit:
                    ls.survival_selection(cmb_1)
                if ls.fitness(cmb_2) > ls.best_fit:
                    ls.survival_selection(cmb_2)
                    
        print("----------------------------------------")
        print("Best fit: ", ls.best_fit)
        print("Fit calls: ", ls.fitness.calls)