from scripts.lib.family_script_schema import FamilyScript


def test_family_script_roundtrip():
    script = FamilyScript(
        family_id="FAM_JESSICA",
        canonical_name="Jessica",
        root_name="Iscah",
        root_language="Hebrew",
        meaning_core=["to behold", "foresight"],
        historical_path=["Biblical Hebrew", "English Renaissance"],
        family_fun_fact="Popularized by Shakespeare."
    )

    restored = FamilyScript.from_dict(script.to_dict())

    assert restored.family_id == script.family_id
    assert restored.meaning_core == script.meaning_core
    assert restored.family_fun_fact == script.family_fun_fact
