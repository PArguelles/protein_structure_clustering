
import random
import numpy as np
import matplotlib.pyplot as plt

# GENETIC ALGORITHM
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# PROTEIN CLUSTERING
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering

samples = ['a.1','a.3','b.2','b.3']

clustering = ['complete','average']

combinations = [('rmsd','gdt_2'),('rmsd','gdt_4'),
                ('rmsd','maxsub'),('rmsd','tm'),
                ('gdt_2','gdt_4'),('gdt_2','maxsub'),
                ('gdt_2','tm'), ('gdt_4','maxsub'),
                ('gdt_4','tm'), ('maxsub','tm')]

NGENERATIONS = 30
POPSIZE = 100

for measures in combinations:
    for alg in clustering:
        for spl in samples:

            #####################################################
            # LOAD PROTEIN DATA
            #####################################################
            measure1 = measures[0]
            measure2 = measures[1]
            measure3 = 'seq'
            algorithm = alg
            sample_for_domains = spl
            sample = spl+'.'  
            #path_to_results = 'C:/ShareSSD/scop/genetic_results_pair/small_gen_'+alg+'_'+sample+'_'+measure1+'_'+measure2       
            matrix1 = rs.loadMatrixFromFile(sample, measure1)
            matrix2 = rs.loadMatrixFromFile(sample, measure2)
            matrix3 = rs.loadMatrixFromFile(sample, measure3)
            matrix1 = mf.minMaxScale(matrix1)
            matrix2 = mf.minMaxScale(matrix2)
            matrix3 = mf.minMaxScale(matrix3)
            matrix1 = mf.calculateDistances(matrix1)
            matrix2 = mf.calculateDistances(matrix2)
            matrix3 = mf.calculateDistances(matrix3)
            domains = rs.loadDomainListFromFile(sample_for_domains)
            n_labels = scop.getUniqueClassifications(sample_for_domains)
            ground_truth = scop.getDomainLabels(domains)

            current_individual = 0
            current_generation = 0
            #writer = open(path_to_results, 'w') 
            #writer.write('Gen: '+str(current_generation)+'\n')

            #####################################################
            # GENETIC ALGORITHM
            #####################################################

            IND_SIZE = 3  
            toolbox = base.Toolbox()
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMax)
            toolbox.register("attr_bool", random.uniform, 0, 1)
            toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=IND_SIZE)
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)

            def evaluate(individual):

                indv = [round(x,2) for x in individual]
                w1 = indv[0]
                w2 = indv[1]
                w3 = indv[2]

                #w2 = 1 - w1
                #w3 = 0

                corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)
                if algorithm == 'complete':      
                    agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(corr)
                    labels = agglomerative.labels_
                elif algorithm == 'average':
                    agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='average').fit(corr)
                    labels = agglomerative.labels_
                elif algorithm == 'kmedoids':
                    _, clusters = km.kMedoids(corr, n_labels, 100)
                    labels = km.sortLabels(clusters)
                metrics = ce.clusterEvaluation(corr, labels, ground_truth)

                global current_individual  
                global current_generation  
                global POPSIZE
                
                return float(metrics[4]),

            toolbox.register("evaluate", evaluate)
            toolbox.register("mate", tools.cxTwoPoint)
            toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)
            toolbox.register("select", tools.selTournament, tournsize=40)
            #toolbox.register("select", tools.selBest)
            #toolbox.register("select", tools.selBest)
            

            def main():
                random.seed(94)

                global NGENERATIONS
                global POPSIZE

                population = toolbox.population(n=POPSIZE)

                # CXPB - probabilidade de crossover
                # MUTPB - probabilidade de mutacao
                # NGEN - numero de geracoes
                CXPB, MUTPB = 0.9, 0.01
                
                # STATISTICS
                stats = tools.Statistics(key=lambda ind: ind.fitness.values)
                #stats.register("std", np.std)
                stats.register("min", np.min)
                stats.register("avg", np.mean)
                stats.register("max", np.max)

                # Run GA
                population, logbook = algorithms.eaSimple(population, toolbox, CXPB, MUTPB, NGENERATIONS, stats=stats)
                
                gen = logbook.select("gen")
                min = logbook.select("min")
                avg = logbook.select("avg")
                max = logbook.select("max")

                with open('C:/ShareSSD/scop/genetic_results_pair_avg/genetic_'+alg+'_'+spl+'_'+measure1+'_'+measure2, 'w') as nf:
                    for g, mi, a, ma in zip(gen, min, avg, max):
                        nf.write(str(g)+' '+str(mi)+' '+str(a)+' '+str(ma)+'\n')

                    for indv in population:
                        nf.write('Indv: '+str(indv[0])+' '+str(indv[1])+' '+str(indv[2])+'\n')

            if __name__ == "__main__":
                main()