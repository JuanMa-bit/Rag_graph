import pymongo
from pymongo.errors import ServerSelectionTimeoutError
import json

credentials_path="/Users/jucampo/Desktop/Ideas/Podcast/RAG_GRAPH/Rag_graph/credentials/credentials.json"
with open(credentials_path, 'r') as file:
    credentials = json.load(file)

uri = credentials["pymongo"]["uri"]

class PymongoConnection():
    

    def __init__(self) -> None:
        self.myclient = pymongo.MongoClient(uri)
    def verify_connection(self):
        try:
            info = self.myclient.server_info()
            print("server is up.")
        except ServerSelectionTimeoutError:
            print("server is down.")
    def create_db(self, name_db) -> None:
        mydb = self.myclient[name_db]
    def verify_db_exist(self, name_db) ->None:
        dblist = self.myclient.list_database_names()
        if name_db in dblist:
            print("The database exists.")
        else:
            print("The database not exists.")
    def get_db_list(self) -> list:
        return self.myclient.list_database_names()
    def create_collection(self, name_db, name_collection) -> None:
        mydb = self.myclient[name_db]
        mycol = mydb[name_collection]
    def verify_collection_exist(self, name_db, name_collection) ->None:
        mydb = self.myclient[name_db]
        collist = mydb.list_collection_names()
        if name_collection in collist:
            print("The collection exists.")
        else: 
            print("The collection not exists")
    def insert_many_documents(self, name_db, name_collection, document_list) ->None:
        mydb = self.myclient[name_db]
        mycol = mydb[name_collection]
        x = mycol.insert_many(document_list)