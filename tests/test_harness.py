import hashlib
import pickle
import platform
import sys
import pytest

# Import the data from your src folder
from src.fixtures import TEST_DATA, Fruit

# --- Helper Functions ---
def roundtrip(obj, protocol):
    data = pickle.dumps(obj, protocol=protocol)
    return pickle.loads(data)

# --- Test Fixtures ---
@pytest.fixture
def test_data():
    return TEST_DATA

@pytest.fixture
def protocol():
    return 4


# --- Pytest Test Cases ---

def test_dict_roundtrip(test_data, protocol):
    original = test_data["dict"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original

def test_string_roundtrip(test_data, protocol):
    original = test_data["string"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original

def test_int_roundtrip(test_data, protocol):
    original = test_data["int"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original

def test_float_roundtrip(test_data, protocol):
    original = test_data["float"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original
    
def test_tuple_roundtrip(test_data, protocol):
    original = test_data["tuple"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original

def test_cursed_list_roundtrip(test_data, protocol):
    original = test_data["cursed_list"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original

def test_class_instance_roundtrip(test_data, protocol):
    original = test_data["class_instance"]
    loaded = roundtrip(original, protocol)
    assert type(loaded) is type(original)
    assert loaded == original