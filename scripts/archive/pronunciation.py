from __future__ import annotations

import re
from scripts.lib.knowledge import KnowledgeRecord

# Базове перетворення CMU → IPA
CMU_TO_IPA = {
    "AA":"ɑ","AE":"æ","AH":"ə","AO":"ɔ","AW":"aʊ","AY":"aɪ",
    "B":"b","CH":"tʃ","D":"d","DH":"ð","EH":"ɛ","ER":"ɝ",
    "EY":"eɪ","F":"f","G":"ɡ","HH":"h","IH":"ɪ","IY":"i",
    "JH":"dʒ","K":"k","L":"l","M":"m","N":"n","NG":"ŋ",
    "OW":"oʊ","OY":"ɔɪ","P":"p","R":"r","S":"s","SH":"ʃ",
    "T":"t","TH":"θ","UH":"ʊ","UW":"u","V":"v","W":"w",
    "Y":"j","Z":"z","ZH":"ʒ"
}

STRESS = {"1":"ˈ","2":"ˌ"}

def cmu_to_ipa(phonetic: str | None) -> str | None:
    if not phonetic:
        return None

    ipa = []

    for token in phonetic.split():
        m = re.match(r"([A-Z]+)([012]?)", token)
        if not m:
            continue

        phoneme, stress = m.groups()

        if stress in STRESS:
            ipa.append(STRESS[stress])

        ipa.append(CMU_TO_IPA.get(phoneme, ""))

    return "/" + "".join(ipa) + "/"

def human_pronunciation(name: str) -> str:
    """Simple readable fallback."""

    custom = {
        "Amelia": "uh-MEE-lee-uh",
        "Sophia": "so-FEE-uh",
        "Liam": "LEE-um",
        "Noah": "NOH-uh",
        "Olivia": "oh-LIV-ee-uh",
    }

    return custom.get(name, name)

def enrich_pronunciation(record: KnowledgeRecord, phonetic: str | None):
    record.ipa = cmu_to_ipa(phonetic)
    record.pronunciation = human_pronunciation(record.name)
    return record