import pytest
from unittest.mock import Mock

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    redis_mock = Mock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.setex.return_value = True
    
    def mock_redis_client(*args, **kwargs):
        return redis_mock
    
    monkeypatch.setattr("app.cache.Redis", mock_redis_client) 