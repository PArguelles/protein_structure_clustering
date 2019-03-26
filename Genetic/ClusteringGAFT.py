
# GENETIC ALGORITHM
from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import DecimalIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import RouletteWheelSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation
from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis
from gaft.analysis.fitness_store import FitnessStore

# PROTEIN CLUSTERING
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering

#####################################################
# LOAD PROTEIN DATA
#####################################################

path_to_results = 'C:/ShareSSD/scop/genetic_results/'
measure1 = 'rmsd'
measure2 = 'gdt_2'
measure3 = 'seq'
algorithm = 'complete'
sample = 'a.1.'
sample_for_domains = 'a.1'
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

#####################################################
# GENETIC ALGORITHM CONFIG
#####################################################

while True:

    try:

        # Define population.
        indv_template = DecimalIndividual(ranges=[(0.1, 0.9),(0.1, 0.9),(0.1, 0.9)], eps=[0.01,0.01,0.01])
        population = Population(indv_template=indv_template, size=20).init()

        # Create genetic operators.
        #selection = TournamentSelection()
        selection = RouletteWheelSelection()
        crossover = UniformCrossover(pc=0.8, pe=0.5)
        mutation = FlipBitMutation(pm=0.02)

        # Create genetic algorithm engine.
        engine = GAEngine(population=population, selection=selection, crossover=crossover, mutation=mutation, analysis=[FitnessStore])

        current_iteration = 0

        writer = open(path_to_results+algorithm+'_'+sample+'_'+measure1+'_'+measure2, 'w')

        # Define fitness function.
        @engine.fitness_register
        def fitness(indv):
            w1, w2, w3 = indv.solution
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

            global current_iteration
            writer.write(str(current_iteration)+': '+str(w1)+' '+str(w2)+' '+str(w3)+' '.join(str(x) for x in metrics)+'\n')
            current_iteration += 1

            return float(metrics[0]) * 100

        # Define on-the-fly analysis.
        @engine.analysis_register
        class ConsoleOutputAnalysis(OnTheFlyAnalysis):
            interval = 1
            master_only = True

            def register_step(self, g, population, engine):
                best_indv = population.best_indv(engine.fitness)
                msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.ori_fmax)
                print(msg)
                writer.write(msg)
                writer.write(str(best_indv.chromsome)+'\n')
                #print(str(best_indv[0])+str(best_indv[1])+str(best_indv[2]))
                #self.logger.info(msg)

            # added path
            def finalize(self, population, engine):
                best_indv = population.best_indv(engine.fitness)
                x = best_indv.solution
                y = engine.ori_fmax
                msg = 'Optimal solution: ({}, {})'.format(x, y)

                writer.write(str(x)+'\n')

                print(msg)
                print(x)
                #self.logger.info(msg)

        if '__main__' == __name__:
            # Run the GA engine.
            engine.run(ng=20)

        writer.close()
        break

    except:
        pass
