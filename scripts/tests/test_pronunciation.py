from scripts.lib.pronunciation import cmu_to_ipa

def test_cmu_to_ipa():
    assert cmu_to_ipa("AH0 M IY1 L IY0 AH0") == "/əmˈiliə/"