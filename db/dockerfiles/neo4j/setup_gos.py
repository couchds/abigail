from neo4j import GraphDatabase

URI = 'neo4j://neo4j:7687'

def setup_gos():
    query = '''
        USING PERIODIC COMMIT 500
        LOAD CSV WITH HEADERS FROM 'file:///go-basic.tsv' AS row FIELDTERMINATOR '\t' 
        WITH row  WHERE row.name IS NOT NULL AND row.synonyms IS NOT NULL
        MERGE (g:GO {uid: row.id, name: row.name, namespace: row.namespace, definition: row.definition})
        WITH g, row
        UNWIND split(row.synonyms, "&&") as synonym
        MERGE (s: Synonym {name: synonym})
        MERGE (g)-[:has_synonym]->(s)
    '''
    driver = GraphDatabase.driver(URI, auth=("neo4j", "tmppassword"), encrypted=False) # encrypted set to false for localhost
    with driver.session() as session:
        session.run(query)

setup_gos()