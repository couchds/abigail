from neo4j import GraphDatabase


URI = 'neo4j://neo4j:7687' # use the neo4j container

INDICES = [
    {
        'node_label': 'GO',
        'property': 'uid'
    },
    {
        'node_label': 'Gene',
        'property': 'name'
    },
    {
        'node_label': 'Disease',
        'property': 'name'
    },
    {
        'node_label': 'Synonym',
        'property': 'name'
    }
]


def create_index_query(node_type, indexed_property):
    """ Create the query for the index statement. See:
    https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/
    """
    print(f'CREATE INDEX ON :{node_type}({indexed_property});')
    return f'CREATE INDEX ON :{node_type}({indexed_property});'


def setup_indices():
    driver = GraphDatabase.driver(URI, auth=("neo4j", "tmppassword"), encrypted=False) # encrypted set to false for localhost
    with driver.session() as session:
        for index in INDICES:
            session.run(create_index_query(index['node_label'], index['property']))