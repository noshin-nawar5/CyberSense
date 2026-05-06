"""
Backend API Tests
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
import json
import pytest


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test home endpoint returns status"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'online'


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'
    assert 'models' in data


def test_predict_valid_text(client):
    """Test prediction with valid text"""
    response = client.post('/api/predict',
        data=json.dumps({'text': 'This is a test message'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'confidence' in data
    assert data['prediction'] in ['cyberbullying', 'not_cyberbullying']
    assert 0 <= data['confidence'] <= 1


def test_predict_missing_text(client):
    """Test prediction with missing text field"""
    response = client.post('/api/predict',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_predict_empty_text(client):
    """Test prediction with empty text"""
    response = client.post('/api/predict',
        data=json.dumps({'text': ''}),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_predict_long_text(client):
    """Test prediction with text exceeding max length"""
    long_text = 'a' * 6000  # Exceeds 5000 char limit
    response = client.post('/api/predict',
        data=json.dumps({'text': long_text}),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_batch_predict_valid(client):
    """Test batch prediction with valid texts"""
    response = client.post('/api/batch-predict',
        data=json.dumps({
            'texts': ['text 1', 'text 2', 'text 3']
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert len(data['results']) == 3
    assert data['count'] == 3


def test_batch_predict_too_many(client):
    """Test batch prediction with too many texts"""
    texts = ['text'] * 150  # Exceeds 100 limit
    response = client.post('/api/batch-predict',
        data=json.dumps({'texts': texts}),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_404_endpoint(client):
    """Test 404 for non-existent endpoint"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_method_not_allowed(client):
    """Test wrong HTTP method"""
    response = client.get('/api/predict')
    assert response.status_code == 405


def test_safe_text_prediction(client):
    """Test prediction for safe text"""
    response = client.post('/api/predict',
        data=json.dumps({'text': 'You are amazing and talented!'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    # In demo mode, this should be classified as not_cyberbullying
    assert 'prediction' in data


def test_harmful_text_prediction(client):
    """Test prediction for potentially harmful text"""
    response = client.post('/api/predict',
        data=json.dumps({'text': 'You are stupid and ugly'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
