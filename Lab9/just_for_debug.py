import random
from random import choices
import lab9_lib

PROBLEM_SIZES = [1, 2, 5, 10]
LOCI = 1000

class LocalSearch:
    def __init__(self, mut_rate, cmb_rate, blck_size):
        self.mutation_rate = mut_rate
        self.combination_rate = cmb_rate
        #Block size expressed in percentage
        self.block_size = blck_size
        self.population = []

    def generate_population(self, n_individuals):
        for _ in range(n_individuals):
            self.population.append(choices([0, 1], k=LOCI))

    #Function that receives a genome ad return a mutated version of it accordingly to a random choice and a mutation paremeter
    def mutate(self, genome):
        mutated_genome = []

        for e in genome:
            if random.random() > self.mutation_rate:
                mutated_genome.append(not e)
            else:
                mutated_genome.append(e)

        return mutated_genome

    #TO DO unisci queste due funzioni di combine

    #Function that receives two genomes and returns a combined version of the two.
    #The combination happens at a very specific level. In fact each element (bit from 
    # our poit of view) of the genome is taken into consideration before swapping.
    def combine_genomes_bit_level(self, gen_1, gen_2):
        combined_1 = []
        combined_2 = []

        for i in range(len(gen_1)):
            if random.random() > self.combination_rate:
                tmp = gen_1[i]
                gen_1[i] = gen_2[i]
                gen_2[i] = tmp

        return combined_1, combined_2

    #Function that receives two genomes and returns a combined version of the two.
    #The combination happens at block level. Same as above, but instead of varying
    #at bit level, it varies a sequence of bits.
    def combine_genomes_block_level(self, gen_1, gen_2):
        combined_1 = []
        combined_2 = []
        bound = int(self.block_size*len(gen_1))
        start = 0

        for _ in range(len(gen_1)/bound):
            if random.random() > self.combination_rate:
                tmp = gen_1[start:bound]
                gen_1[start:bound] = gen_2[start:bound]
                gen_2[start:bound] = tmp
            start += bound

        return combined_1, combined_2
    
    def parent_selection():
        print("do something")

    def run():
        print("Do things")

if __name__ == "__main__":
    for problem_size in PROBLEM_SIZES:
        fitness = lab9_lib.make_problem(problem_size)

        #In teoria al posto di quesot cfor devi continuare finchè non risolvi, quindi diventa while
        for n in range(problem_size):
            ind = choices([0, 1], k=50)
            ind_1 = choices([0, 1], k=50)
            ind_2 = choices([0, 1], k=50)

            LocalSearch.mutate(ind)
            LocalSearch.combine_genomes_bit_level(ind_1, ind_2)
            LocalSearch.combine_genomes_block_level(ind_1, ind_2)

            #Fatti restituire il valore della fitness, ma trattala come se non la conoscessi, analizzi il risultato e bom
            print(f"{''.join(str(g) for g in ind)}: {fitness(ind):.2%}")

        print(fitness.calls)