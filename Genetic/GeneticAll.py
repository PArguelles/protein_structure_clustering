
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

#'a.1','a.3','b.2','b.3'
samples = ['a.1','a.3','b.2','b.3']

clustering = ['kmedoids']

measures = ['rmsd','gdt_2','gdt_4','maxsub','tm']

NGENERATIONS = 30
POPSIZE = 200


for alg in clustering:
    for spl in samples:

        #####################################################
        # LOAD PROTEIN DATA
        #####################################################
        measure1 = measures[0]
        measure2 = measures[1]
        measure3 = measures[2]
        measure4 = measures[3]
        measure5 = measures[4]

        algorithm = alg
        sample_for_domains = spl
        sample = spl+'.'  
        path_to_results = 'C:/ShareSSD/scop/genetic_results_all/gen3_'+alg+'_'+spl

        matrix1 = rs.loadMatrixFromFile(sample, measure1)
        matrix2 = rs.loadMatrixFromFile(sample, measure2)
        matrix3 = rs.loadMatrixFromFile(sample, measure3)
        matrix4 = rs.loadMatrixFromFile(sample, measure4)
        matrix5 = rs.loadMatrixFromFile(sample, measure5)

        matrix1 = mf.minMaxScale(matrix1)
        matrix2 = mf.minMaxScale(matrix2)
        matrix3 = mf.minMaxScale(matrix3)
        matrix4 = mf.minMaxScale(matrix4)
        matrix5 = mf.minMaxScale(matrix5)

        matrix1 = mf.calculateDistances(matrix1)
        matrix2 = mf.calculateDistances(matrix2)
        matrix3 = mf.calculateDistances(matrix3)
        matrix4 = mf.calculateDistances(matrix4)
        matrix5 = mf.calculateDistances(matrix5)

        domains = rs.loadDomainListFromFile(sample_for_domains)
        n_labels = scop.getUniqueClassifications(sample_for_domains)
        ground_truth = scop.getDomainLabels(domains)

        current_individual = 0
        current_generation = 0

        #####################################################
        # GENETIC ALGORITHM
        #####################################################

        IND_SIZE = 5  
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
            w4 = indv[3]
            w5 = indv[4]

            global matrix1 
            m1 = matrix1 * w1
            global matrix2
            m2 = matrix2 * w2
            global matrix3
            m3 = matrix3 * w3
            global matrix4
            m4 = matrix4 * w4
            global matrix5
            m5 = matrix5 * w5

            corr = m1 + m2 + m3 + m4 + m5

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
            
            if current_individual == POPSIZE:
                current_individual = 0
                current_generation += 1
            current_individual += 1
            print(current_individual)
            #mtr = [round(m,2) for m in metrics]
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
            global writer

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