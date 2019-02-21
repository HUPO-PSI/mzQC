import pytest
import os 

def test_single_idfree():
    assert os.path.isfile('schema/current/examples/single_idfree.qc.json')

def test_multi_idfree():
    assert os.path.isfile('schema/current/examples/multi_idfree.qc.json')


