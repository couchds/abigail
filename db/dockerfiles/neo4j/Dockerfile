FROM neo4j:4.3.7

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip
RUN pip install neo4j-driver
RUN pip install Bio

COPY ./data/gene_output.tsv /var/lib/neo4j/import
COPY ./data/doid.tsv /var/lib/neo4j/import
COPY ./data/go-basic.tsv /var/lib/neo4j/import

# also copying over setup scripts for testing
COPY ./setup_gos.py /var/lib/neo4j
COPY ./setup_genes.py /var/lib/neo4j
COPY ./setup_diseases.py /var/lib/neo4j
COPY ./setup_pubmeds.py /var/lib/neo4j