from dots_editor import core, utf8_braille
import os, pygame, pytest

TEST_STRING = u'\u2801\u2803\u2809\u2819\u2811'

def test_setenv():
    assert os.environ["SDL_VIDEODRIVER"] == "dummy"

def test_key_to_dot(game):
    assert game.key_to_dot(pygame.K_f) == 1
    assert game.key_to_dot(pygame.K_d) == 2
    assert game.key_to_dot(pygame.K_s) == 3
    assert game.key_to_dot(pygame.K_j) == 4
    assert game.key_to_dot(pygame.K_k) == 5
    assert game.key_to_dot(pygame.K_l) == 6

def test_sentence_to_lines_single_line(game):
    lines = game.sentence_to_lines()
    assert len(lines) == 1
    assert lines[0] == TEST_STRING

def test_sentence_to_lines_double_line(game):
    line1 = u'\u2840'*40
    line2 = u'\u2840'*3
    game.sentence = make_cells(line1 + line2)
    lines = game.sentence_to_lines()
    assert len(lines) == 2
    assert lines[0] == line1
    assert lines[1] == line2

def test_ascii_lines(game):
    lines = game.sentence_to_lines()
    a_lines = game.ascii_lines(lines)
    assert len(a_lines) == 1
    assert a_lines[0] == 'ABCDE'

def test_save_sentence_ascii(game, tmpdir):
    assert game.savemode == 'ascii'
    game.save_sentence()
    f = tmpdir.join('test.txt')
    assert f.check()
    assert f.read() == 'ABCDE'

def test_save_sentence_ascii(game, tmpdir):
    game.savemode = 'unicode'
    game.save_sentence()
    f = tmpdir.join('test.txt')
    assert f.check()
    assert f.read_text('utf8') == TEST_STRING

def test_draw_sentence(game):
    # not that we can see the lines, just that it doesn't throw errors
    game.draw_sentence()
    assert True

def make_cells(chars):
    return [utf8_braille.Cell(c) for c in chars]

@pytest.fixture
def game(tmpdir):
    f = tmpdir.join('test.txt')
    game = core.Game(str(f), 'ascii')
    game.sentence = make_cells(u'\u2801\u2803\u2809\u2819\u2811')
    return game
