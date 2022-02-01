""" Convert genes from HGNC's TSV format into one more suitable for neo4j import.
"""

from posixpath import split


GENE_FNAME = 'custom.txt'

def transform_genes():
    with open(GENE_FNAME, 'r', encoding="utf8") as infile:
        with open('gene_output.tsv', 'w', encoding="utf8") as outfile:
            for i, line in enumerate(infile):
                if i == 0:
                    outfile.write('uid\tapproved_symbol\tapproved_name\tsynonyms\n')
                else:
                    split_line = line.strip('\n').split('\t')
                    previous_symbols = split_line[4].split(', ')
                    alias_symbols = split_line[5].split(', ')
                    alias_names = split_line[9].replace('"', '').split(', ')
                    synonyms = list(set(previous_symbols) | set(alias_symbols) | set(alias_names))
                    print(synonyms)
                    outfile.write('\t'.join([
                        split_line[0],
                        split_line[1],
                        split_line[2],
                        ('&'.join(synonyms)).lstrip('&')
                    ])+'\n')

transform_genes()
