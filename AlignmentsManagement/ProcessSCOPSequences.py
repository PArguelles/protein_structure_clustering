

def createSequencesFile(sample):
    path_to_sample = 'C:/ShareSSD/scop/data/domains_'+sample
    path_to_sequences = 'C:/ShareSSD/scop/sequences_'+sample
    path_to_sequences_files = 'C:/ShareSSD/scop/sequences/'

    with open(path_to_sequences, 'w') as fp:

        with open(path_to_sample, 'r') as fp2:

            line = fp2.readline()
            while line:
                print(line)
                domain = str(line).strip()
                with open(path_to_sequences_files+domain, 'r') as fp3:
                    line2 = fp3.readline()
                    while line2:
                        fp.write(line2)
                        line2 = fp3.readline()

                line = fp2.readline()

def processSCOPSequences():
    path_to_sequences = 'C:/ShareSSD/scop/scope/astral-scopedom-seqres-gd-all-2.07-stable.fa.txt'
    path_to_files = 'C:/ShareSSD/scop/sequences/'

    with open(path_to_sequences, 'r') as fp:

        line = fp.readline()
        while line:
            if '>' in line:
                domain_id = str(line).strip().split()[0][1:]
                with open(path_to_files+domain_id+'.ent', 'w') as nf:
                    while line:
                        nf.write(str(line))
                        print(line)
                        line = fp.readline()
                        if '>' in line:
                            break
            else: break

def createStructureList(sample):
    path_to_sample = 'C:/ShareSSD/scop/samples/sample_structures_'+sample
    path_to_new = 'C:/ShareSSD/scop/structures_'+sample
    
    with open(path_to_new, 'w') as fp:
        with open(path_to_sample, 'r') as fp2: 
            line = fp2.readline()
            while line:
                fp.write('C:/ShareSSD/scop/structures/'+str(line))
                line = fp2.readline()
