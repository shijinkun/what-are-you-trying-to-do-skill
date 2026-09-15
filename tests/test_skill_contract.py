from pathlib import Path


SKILL = Path(__file__).parents[1] / "SKILL.md"


def test_skill_is_domain_neutral_and_has_required_boundary_checks():
    text = SKILL.read_text(encoding="utf-8")
    required = [
        "construct validity",
        "measurement invariance",
        "operational indicator",
        "comparison axis",
        "fixed or recorded conditions",
        "exactly one",
        "if_start",
        "start_authority",
        "do not invent",
        "chain-of-thought",
    ]
    for phrase in required:
        assert phrase.lower() in text.lower(), phrase


def test_skill_does_not_hard_code_materials_domain_or_downstream_pipeline():
    text = SKILL.read_text(encoding="utf-8").lower()
    forbidden = ["hea-oer", "ecsa", "tafel slope", "mineru", "deepseek"]
    for phrase in forbidden:
        assert phrase not in text, phrase


def test_skill_declares_human_authorization_and_unknown_uncertainty():
    text = SKILL.read_text(encoding="utf-8").lower()
    for phrase in ["human", "authorized", "unknown", "json"]:
        assert phrase in text, phrase


def test_skill_is_written_for_anyone_formulating_a_question_to_ai():
    text = (SKILL.parent / "README.md").read_text(encoding="utf-8").lower()
    assert "向 ai 提问" in text
    assert "swissguard" not in text
    assert "hea" not in text


def test_skill_calibrates_claim_language_to_evidence_strength():
    text = SKILL.read_text(encoding="utf-8").lower()
    required = [
        "research design",
        "sample size",
        "methodological quality",
        "risk of bias",
        "consistency and reproducibility",
        "scope of inference",
        "wording",
        "causal",
        "consensus",
        "uncertainty",
    ]
    for phrase in required:
        assert phrase in text, phrase
