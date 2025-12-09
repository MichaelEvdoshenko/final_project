from src.core.game import Krestik_nolik

def test_3x3_win():
    game = Krestik_nolik(3)
    game.make_move(0, 0, 'X')
    game.make_move(1, 0, 'O') 
    game.make_move(0, 1, 'X')
    game.make_move(1, 1, 'O')
    game.make_move(0, 2, 'X')
    assert game.winner == 'X'

def test_draw():
    game = Krestik_nolik(3)
    moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,1), (2,0), (2,2)]
    for i, (r, c) in enumerate(moves):
        game.make_move(r, c, 'X' if i % 2 == 0 else 'O')
    assert game.winner == "НИЧЬЯ"

if __name__ == "__main__":
    test_3x3_win()
    test_draw()
    print("Все тесты прошли!")