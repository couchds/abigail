# import packages
from Bio import Entrez
from neo4j import GraphDatabase, basic_auth
import nltk
#nltk.download('wordnet')
#nltk.download('words')
#from nltk.corpus import words
from nltk.corpus import wordnet as wd
import time
#ALL_WORDS = set(words.words())
Entrez.email = "danielcouch1864@gmail.com"
Entrez.api_key = '3413e767905d62a46441e83b7b2cd05d6608'
# set up driver
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=basic_auth("neo4j", "tmppassword"), encrypted=False)
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]
        

# TODO: NLP/filtering
# Gene/disease pubmed relations now set up;
# Only working with GO synonyms now.
#
try:
    with open('searched_names.txt', 'r') as rfile:
        lines = [line.strip() for line in rfile.readlines()]
except FileNotFoundError:
    lines = []
session = driver.session()
synonyms = [s for s in session.run("MATCH (n: Synonym) RETURN n.name AS name")]
current_index = 0
counter = 0
for index, s_syn in enumerate(synonyms):
    name = s_syn["name"]
    print(index)
    print(name)
    if name in lines:
        print("FOUND: " + name)
        continue
    if index % 1000 == 0:
        print(index)
        print(name)
    # simple word validation check
    if len(wd.synsets(name)) > 0 or 0 < len(name) < 4:
        print("Invalid:" + name)
        continue
    if name.isdigit():
        continue
    # efetch search pubmed
    # add " " to the string and search title/abstract only now. limit the results to 10,00,000
#    try: 
    result = Entrez.esearch(db="pubmed", term="\"%s\"[title/abstract]"%(name), retmax=1000000)
#    except Exception as e:
#        with open('errors.txt', 'a') as eoufile:
#            eoufile.write('---\nName:%s\n---Exception:%s\n---\n' % (name, str(e)))
#        time.sleep(30)
#        continue
    # moved out of try...
    id_list = Entrez.read(result)["IdList"]
    if id_list:
        id_chunks = chunks(id_list, 10000)
        # generate the id_list into a chuck size of 10,000
        for s_chunk in id_chunks:
            #  create the relationship and if node not exist, creat the node
            #for s_id in s_chunk:
            tx = session.begin_transaction()
            tx.run("WITH $s_chunk AS coll \
                                    UNWIND coll AS x \
                                    WITH x \
                                    MATCH (from:Synonym { name: \"%s\"}) \
                                   MERGE (to:Pubmed { id: x}) \
                                   MERGE (from)-[r:associated_with_pubmed]->(to)" % (name), s_chunk=s_chunk)
            tx.commit()
            tx.close()
                    #tx.run(syn_pubmed_rel)
                    #tx.commit()
                    #tx.close()
            for s_id in s_chunk:
                #with open('efetch_data/syns_{}.txt'.format(current_index), 'a+') as outfile:
                #    outfile.write('{}\t{}\n'.format(name, s_id))
                counter += 1
                if (counter == 1000000):
                    counter = 0
                    current_index += 1
    result.close()
#    except Exception as e:
#        with open('xml_problem.txt', 'a') as eoufile:
#            eoufile.write('---\nName:%s\n---Exception:%s\n---\n' % (name, str(e)))
#        continue
    try:
        with open('searched_names.txt', 'a') as ofile:
            ofile.write(name + '\n')
    except:
        pass
    if index % 10000 == 0:
        print(index)
        time.sleep(10)
    print("End of loop")
session.close()