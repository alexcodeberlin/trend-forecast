from elasticsearch_dsl import connections
from config import ES_HOST

def init_es():
    connections.create_connection(
        alias="default",
        hosts=[ES_HOST]
    )