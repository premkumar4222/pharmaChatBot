# from neo4j import GraphDatabase

# URI = "neo4j+s://fff54318.databases.neo4j.io"
# AUTH = ("neo4j", "btoVD5XT_JDuHp6gKvPpGSyqjfHCfAxeBcR529tCdn0")

# driver = GraphDatabase.driver(URI, auth=AUTH)
# driver.verify_connectivity()

from neo4j import GraphDatabase

uri = "neo4j+s://fff54318.databases.neo4j.io"
auth = ("neo4j", "btoVD5XT_JDuHp6gKvPpGSyqjfHCfAxeBcR529tCdn0")

driver = GraphDatabase.driver(uri, auth=auth)
driver.verify_connectivity()
print("Connection successful!")

