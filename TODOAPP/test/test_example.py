import pytest


def test_equal_or_notequal():
    assert 3!=1
    assert 3 == 3

def test_is_instance():
    assert isinstance("This is real shit",str)
    assert not isinstance("10", int)

def test_boolean():
    validated = True
    assert validated is True
    assert ("Hello" == "World") is False


def test_type():
    assert type("Hello" is str)
    assert type(10 is int)

def test_greater_than_and_less_than():
    assert 10 > -10
    assert -5 < -4.5

def test_list() :
    num_list = [1,2,3,4,5]
    any_list = [False,False]
    assert 1 in  num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self,first_name:str,last_name:str,major:str,years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture()
def default_intern():
        return Student("Bhawish","Kumar", "Computer Science", 3)

def test_person_initialization(default_intern):
    assert default_intern.first_name == "Bhawish","First name should be Bhawish"
    assert default_intern.last_name == "Kumar", "First name should be Kumar"
    assert default_intern.major == "Computer Science"
    assert default_intern.years == 3



