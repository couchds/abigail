from neo4j import GraphDatabase

URI = 'neo4j://neo4j:7687'

def setup_genes():
    query = '''
        USING PERIODIC COMMIT 
        LOAD CSV FROM 'file:///hgnc-extract-12-13-2021.txt' AS row FIELDTERMINATOR '\t'
        MERGE (g:Gene {uid: row[0], symbol: row[1], name: row[2], status: row[3]})
        WITH g, SPLIT(row[4], ", ") AS previous_symbols
        UNWIND previous_symbols as previous_symbol
        MERGE (s: Synonym {name: previous_symbol})
        MERGE (g)-[:has_synonym]->(s)
    '''
    driver = GraphDatabase.driver(URI, auth=("neo4j", "tmppassword"), encrypted=False) # encrypted set to false for localhost
    with driver.session() as session:
        session.run(query)

setup_genes()