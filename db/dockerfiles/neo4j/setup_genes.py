from neo4j import GraphDatabase

URI = 'neo4j://neo4j:7687'

def setup_genes():
    query = '''
        USING PERIODIC COMMIT 
        LOAD CSV WITH HEADERS FROM 'file:///gene_output.tsv' AS row FIELDTERMINATOR '\t'
        MERGE (g:Gene {uid: row.id, symbol: row.approved_symbol, name: row.approved_name})
        WITH g, row
        MERGE (s1: Synonym {name: row.approved_symbol})
        MERGE (g)-[:has_synonym]->(s1)
        WITH g, SPLIT(row.synonyms, "&") AS gene_synonyms
        UNWIND gene_synonyms AS synonym
        MERGE (s2: Synonym {name: synonym})
        MERGE (g)-[:has_synonym]->(s2)
    '''
    driver = GraphDatabase.driver(URI, auth=("neo4j", "tmppassword"), encrypted=False) # encrypted set to false for localhost
    with driver.session() as session:
        session.run(query)

setup_genes()