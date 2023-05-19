from datetime import datetime
from elasticsearch import Elasticsearch

from app.models import Post
from app.search import add_to_index, remove_from_index, query_index

if __name__ == '__main__':
    es = Elasticsearch(
        hosts='https://localhost:9200',
        basic_auth=("elastic", "I=xWY+bRVzGIKkBXytdX"),
        verify_certs=False
    )
    # doc = {
    #     'author': 'kimchy',
    #     'text': 'Elasticsearch: cool. iguana cool.',
    #     'timestamp': datetime.now(),
    # }
    # resp = es.index(index='my_index', id=4, document=doc, human=True)
    # resp = es.index(index='my_index', id=5, document={'text': 'this is a test Boom!'})
    # resp = es.index(index='my_index', id=2, document={'text': 'this is second test'})

    # resp = es.search(index='my_index', body={'query': {'match': {'text': 'second'}}})
    #
    # print(resp)


    # resp = es.index(index="test-index", id=1, document=doc)
    # print(resp['result'])

    # resp = es.search(index="my_index", query={"match_all": {}})
    # print("Got %d Hits:" % resp['hits']['total']['value'])
    # for hit in resp['hits']['hits']:
    #     print(hit["_source"])

    for album in Al.query.all():
        ...
        add_to_index('posts', post)