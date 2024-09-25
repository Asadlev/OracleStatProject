import pytest
from app.main import is_valid_url

# Тестирование функции проверки валидности URL
def test_is_valid_url():
    assert is_valid_url("https://google.com")
    assert is_valid_url("http://localhost")
    assert not is_valid_url("not-a-link")
    assert not is_valid_url("http:/invalid.com")
