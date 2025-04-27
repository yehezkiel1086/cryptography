import mini_aes
import pytest


def test_mini_aes():
    print("test with empty plaintext")
    # empty mini aes
    mini_aes_mockup = mini_aes.MiniAes()

    with pytest.raises(ValueError) as e_info:
        mini_aes_mockup.encrypt()
    assert str(e_info.value) == "plaintext must not be empty"
