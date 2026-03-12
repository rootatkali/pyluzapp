from luzapp.translations.dict_translator import DictTranslator, NullTranslator


def test_dict_translator_subject_hit():
    t = DictTranslator(subjects={"code1": "Full Name"})
    assert t.translate_subject("code1") == "Full Name"


def test_dict_translator_subject_fallback():
    t = DictTranslator(subjects={"code1": "Full Name"})
    assert t.translate_subject("unknown") == "unknown"


def test_dict_translator_group_hit():
    t = DictTranslator(groups={"GroupA": "groupa@example.com"})
    assert t.translate_group("GroupA") == "groupa@example.com"


def test_dict_translator_group_miss():
    t = DictTranslator(groups={"GroupA": "groupa@example.com"})
    assert t.translate_group("GroupB") is None


def test_dict_translator_empty():
    t = DictTranslator()
    assert t.translate_subject("anything") == "anything"
    assert t.translate_group("anything") is None


def test_null_translator_subject():
    t = NullTranslator()
    assert t.translate_subject("code") == "code"
    assert t.translate_subject("") == ""


def test_null_translator_group():
    t = NullTranslator()
    assert t.translate_group("GroupA") is None
    assert t.translate_group("") is None


def test_dict_translator_multiple_subjects():
    t = DictTranslator(
        subjects={"A": "Alpha", "B": "Beta", "C": "Gamma"},
    )
    assert t.translate_subject("A") == "Alpha"
    assert t.translate_subject("B") == "Beta"
    assert t.translate_subject("D") == "D"
