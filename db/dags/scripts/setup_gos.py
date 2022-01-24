from neo4j import GraphDatabase

URI = 'neo4j://neo4j:7687'

def setup_gos():
    query = '''
        USING PERIODIC COMMIT 
        LOAD CSV FROM 'file:///go-basic.tsv' AS row FIELDTERMINATOR '\t' WITH row
        MERGE (g:GO {uid: row[0], name: row[1], namespace: row[2], definition: row[3]})
        WITH g, SPLIT(row[4], ",") AS go_synonyms
        UNWIND go_synonyms as go_synonym
        MERGE (s: Synonym {name: go_synonym})
        MERGE (g)-[:has_synonym]->(s)
    '''
    #with open('')
    print('here!')
    driver = GraphDatabase.driver(URI, auth=("neo4j", "tmppassword"), encrypted=False) # encrypted set to false for localhost
    with driver.session() as session:
        session.run(query)