from neo4j import GraphDatabase, RoutingControl
import json

credentials_path="/Users/jucampo/Desktop/Ideas/Podcast/RAG_GRAPH/Rag_graph/credentials/credentials.json"
with open(credentials_path, 'r') as file:
    credentials = json.load(file)

URI = credentials["Neo4j"]["uri"]
password = credentials["Neo4j"]["auth"]

class Neo4jConnection():

    def __init__(self) -> None:
        self.uri = URI
        self.auth = ('neo4j',password)
        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)

    def verify_connection(self):
        try:
            # Abre una sesión y ejecuta un comando sencillo
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                for record in result:
                    print("La conexión fue exitosa:", record)
        except Exception as e:
            print("Error al conectar a Neo4j:", e)
        finally:
            self.driver.close()
    def add_node(self, tx, type_, entity):
        query = (
            "MERGE (n:{type_} {{entity: $entity}}) "
            "RETURN n"
        ).format(type_=type_)
        result = tx.run(query, entity=entity)
        return result.single()
    def delete_all_nodes(self, tx):
            query1 = "MATCH ()-[r]->() DELETE r"
            query2 = "MATCH (n) DELETE n"
            tx.run(query1)
            tx.run(query2)
    def create_relationship(self, tx, node1_name, type_node1, node2_name, type_node2, relationship_type):
        query = (
            f"MATCH (a:{type_node1} {{entity: $node1_name}}), (b:{type_node2} {{entity: $node2_name}}) "
            f"CREATE (a)-[r:{relationship_type}]->(b)"
        )
        tx.run(query, node1_name=node1_name, node2_name=node2_name)
    def delete_relationship(self, tx, node1_name, type_node1, node2_name, type_node2, relationship_type):
        query = (
            f"MATCH (a:{type_node1} {{entity: $node1_name}})-[r:{relationship_type}]->(b:{type_node2} {{entity: $node2_name}}) "
            "DELETE r"
        )
        tx.run(query, node1_name=node1_name, node2_name=node2_name)
    def add_attributes_to_node(self, tx, node_type, node_name, attributes):
        query = (
            f"MATCH (n:{node_type} {{entity: $node_name}}) "
            "SET " + ", ".join([f"n.{key} = ${key}" for key in attributes.keys()])
        )
        tx.run(query, node_name=node_name, **attributes)
    def add_attribute_to_relationship(self, tx, start_node_id, end_node_id, type_node, relationship_type, attribute_name, attribute_value):
        # Busca la relación entre start_node_id y end_node_id y agrega o actualiza el atributo
        query = (
            "MATCH (x:{type_node} {{entity: $start_node_id}}) "
            "MATCH (y:{type_node} {{entity: $end_node_id}}) "
            "MERGE (x)-[r:{relationship_type}]->(y) "
            "SET r.{attribute_name} = $attribute_value "
            "RETURN r"
        ).format(
            type_node=type_node,
            relationship_type=relationship_type,
            attribute_name=attribute_name
        )
        result = tx.run(query, start_node_id=start_node_id, end_node_id=end_node_id,
                        attribute_value=attribute_value)
        return result.single()
    def execute_operation(self, graph_operation, *args_operation):
        with self.driver.session() as session:
            if graph_operation == "add_node":
                session.write_transaction(self.add_node, *args_operation)
            if graph_operation == "delete_all_nodes":
                session.write_transaction(self.delete_all_nodes)
            if graph_operation == "create_relationship":
                session.write_transaction(self.create_relationship, *args_operation)
            if graph_operation == "delete_relationship":
                session.write_transaction(self.delete_relationship, *args_operation)
            if graph_operation == "add_attributes_to_node":
                session.write_transaction(self.add_attributes_to_node, *args_operation)
            if graph_operation == "add_attribute_to_relationship":
                session.write_transaction(self.add_attribute_to_relationship, *args_operation)
        