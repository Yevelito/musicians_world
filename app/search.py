from app import app
from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    # ... existing code for Elasticsearch indexing

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    # ... existing code for Elasticsearch deletion

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    # ... existing code for Elasticsearch querying