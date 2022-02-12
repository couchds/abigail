from neo4j import GraphDatabase

URI = 'neo4j://neo4j:7687'

def setup_diseases():
    query = '''
        USING PERIODIC COMMIT 
        LOAD CSV WITH HEADERS FROM 'file:///doid.tsv' AS row FIELDTERMINATOR '\t' with row where row.definition is not null
        MERGE (d:Disease {uid: row.id, name: row.name, definition: row.definition})
        WITH d, row
        MERGE (s1: Synonym {name: row.name})
        MERGE (d)-[:has_synonym]->(s1)
        WITH d, SPLIT(row.synonyms, "&&") AS disease_synonyms
        UNWIND disease_synonyms as disease_synonym
        MERGE (s: Synonym {name: disease_synonym})
        MERGE (d)-[:has_synonym]->(s)
    '''
    driver = GraphDatabase.driver(URI, auth=("neo4j", "tmppassword"), encrypted=False) # encrypted set to false for localhost
    with driver.session() as session:
        session.run(query)

setup_diseases()