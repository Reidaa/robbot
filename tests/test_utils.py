from robbot.utils import get_chapter_number


def test_get_chapter_number():
    assert get_chapter_number("Chapter 1") == 1
    assert get_chapter_number("Chapter 1.1") == 1
    assert get_chapter_number("Chapter 1.1.1") == 1
    assert get_chapter_number("Chainsaw Man (last chapter: 123)") == 123


def test_get_chapter_number_2():
    assert get_chapter_number("[DISC] Beat & Motion - Chapter 3") == 3


def test_get_chapter_number_3():
    assert get_chapter_number("[DISC] Tate no Yuusha no Oshinagaki - Chapter 36") == 36

def test_get_chapter_number_colon():
    assert get_chapter_number("[DISC] Overlord - Chapter: 73") == 73


def test_get_chapter_number_abbreviated():
    assert get_chapter_number("[DISC] Mob kara Hajimaru Tansaku Eiyuutan - Ch. 4") == 4




def test_get_chapter_number_6():
    assert get_chapter_number("[DISC] Usogui - Chapter 4") == 4


def test_get_chapter_number_multiple():
    assert get_chapter_number("[DISC] HIGH CARD -♢9 No Mercy - Chapter 1") == 1

def test_get_chapter_number_multiple_2():
    assert get_chapter_number("[DISC] Kaiju No.8 - Chapter 22") == 22


def test_get_chapter_number_empty():
    assert get_chapter_number("") is None
