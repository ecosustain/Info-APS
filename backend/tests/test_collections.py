import pytest
from unittest.mock import Mock, patch
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, InternalServerError

# Import the Collection class from the correct module
from apis.collections import Collection

app = Flask(__name__)

# Seting up Flask app context for testing
ctx = app.app_context()
ctx.push()

def teardown():
    ctx.pop()

@pytest.fixture
def collection():
    collection = Collection()
    return collection

def test_get_all_collections_success(collection):
    with patch('apis.collections.get_all_collections') as mock_get_all_collections:
        mock_get_all_collections.return_value = ['Collection1', 'Collection2']
        result = collection.get()
        expected_result = jsonify(['Collection1', 'Collection2'])
        assert result == expected_result

def test_get_all_collections_not_found(collection):
    with patch('apis.collections.get_all_collections') as mock_get_all_collections:
        mock_get_all_collections.return_value = None
        with pytest.raises(NotFound):
            collection.get()

def test_get_all_collections_internal_error(collection):
    with patch('apis.collections.get_all_collections') as mock_get_all_collections:
        mock_get_all_collections.side_effect = Exception('Internal Server Error')
        with pytest.raises(InternalServerError):
            collection.get()