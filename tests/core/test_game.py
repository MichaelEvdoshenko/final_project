import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.game import Krestik_nolik

def test_game_creation():
    game = Krestik_nolik(3)
    assert game.size == 3
    assert len(game.field) == 3
    assert len(game.field[0]) == 3

def test_game_default_size():
    game = Krestik_nolik()
    assert game.size == 3

def test_game_false_size():
    with pytest.raises(ValueError):
        Krestik_nolik(0)
    
    with pytest.raises(ValueError):
        Krestik_nolik(-1)

def test_game_type():
    with pytest.raises(TypeError):
        Krestik_nolik("три")
    
    with pytest.raises(TypeError):
        Krestik_nolik(3.5)

def test_game_enough_large_size():
    game = Krestik_nolik(5)
    assert game.size == 5
    assert len(game.field) == 5
    assert len(game.field[0]) == 5