import os

class Explore_alignment:
    def __init__(self, query, database, out_file):
        os.system('blastp -db ' + database + ' -query ' + query + ' -out ' + out_file + ' -outfmt "6 qseqid sseqid qstart qend sstart send evalue pident"')
        self.al_file = out_file
        self.aligned_seqs = []
        f = open(self.al_file, 'r')
        line = f.readline()
        while line != '':
            l = line.replace('\n', '').split('\t')
            self.aligned_seqs.append(l)
            line = f.readline()
        f.close()
    
    def extract_entries(self):
        return self.aligned_seqs