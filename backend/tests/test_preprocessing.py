"""
Text Preprocessing Tests
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.preprocessing import (
    clean_text_basic,
    clean_text_advanced,
    clean_text,
    batch_clean_texts
)
import pytest


def test_basic_url_removal():
    """Test URL removal in basic cleaning"""
    text = "Check this out http://example.com"
    result = clean_text_basic(text)
    assert 'http' not in result
    assert 'example.com' not in result


def test_basic_mention_removal():
    """Test mention removal in basic cleaning"""
    text = "Hey @user check this out"
    result = clean_text_basic(text)
    assert '@user' not in result


def test_basic_lowercasing():
    """Test text is lowercased"""
    text = "HELLO WORLD"
    result = clean_text_basic(text)
    assert result == result.lower()


def test_contraction_expansion():
    """Test contraction expansion"""
    text = "I don't think so"
    result = clean_text_basic(text)
    assert 'do not' in result or 'dont' not in result


def test_repeated_char_reduction():
    """Test repeated character reduction"""
    text = "sooooo good"
    result = clean_text_basic(text)
    # Should reduce to at most 2 repeated chars
    assert 'ooo' not in result


def test_whitespace_normalization():
    """Test whitespace normalization"""
    text = "hello    world"
    result = clean_text_basic(text)
    assert '    ' not in result


def test_empty_string():
    """Test empty string handling"""
    result = clean_text_basic("")
    assert result == ""


def test_none_input():
    """Test None input handling"""
    result = clean_text_basic(None)
    assert isinstance(result, str)


def test_numeric_input():
    """Test numeric input handling"""
    result = clean_text_basic(123)
    assert isinstance(result, str)


def test_advanced_cleaning():
    """Test advanced cleaning with NLTK"""
    text = "I don't like this http://test.com"
    result = clean_text_advanced(text)
    assert isinstance(result, str)
    # Should remove URLs and stopwords
    assert 'http' not in result


def test_batch_cleaning():
    """Test batch text cleaning"""
    texts = ["text 1", "text 2", "text 3"]
    results = batch_clean_texts(texts, mode='basic')
    assert len(results) == 3
    assert all(isinstance(r, str) for r in results)


def test_clean_text_modes():
    """Test different cleaning modes"""
    text = "This is a test message @user"
    
    basic = clean_text(text, mode='basic')
    advanced = clean_text(text, mode='advanced')
    
    assert isinstance(basic, str)
    assert isinstance(advanced, str)
    # Both should clean the text
    assert '@user' not in basic
    assert '@user' not in advanced


def test_special_characters():
    """Test special character handling"""
    text = "Hello! How are you? #test"
    result = clean_text_basic(text)
    # Special chars should be removed
    assert '!' not in result
    assert '?' not in result


def test_html_entities():
    """Test HTML entity removal"""
    text = "This &amp; that"
    result = clean_text_basic(text)
    assert '&amp;' not in result


def test_hashtag_handling():
    """Test hashtag handling"""
    text = "This is #awesome"
    result = clean_text_basic(text)
    # Hashtag symbol should be removed, but text might remain
    assert '#' not in result


def test_multiple_urls():
    """Test multiple URL removal"""
    text = "Check http://site1.com and www.site2.com"
    result = clean_text_basic(text)
    assert 'http' not in result
    assert 'www' not in result


def test_mixed_case_preservation():
    """Test that mixed case is converted to lowercase"""
    text = "HeLLo WoRLd"
    result = clean_text_basic(text)
    assert result.islower()


def test_unicode_handling():
    """Test unicode character handling"""
    text = "Hello 🙂 world"
    result = clean_text_basic(text)
    assert isinstance(result, str)


def test_very_long_text():
    """Test handling of very long text"""
    text = "word " * 1000
    result = clean_text_basic(text)
    assert isinstance(result, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
