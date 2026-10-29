import pytest

from pystac.extensions.application import AssetTemplate


def test_create_omits_unspecified_members() -> None:
    template = AssetTemplate.create()
    assert template.to_dict() == {}
    assert template.container is None
    assert template.entrypoint is None
    assert template.languages is None


def test_apply_preserves_omitted_members_and_removes_explicit_none() -> None:
    template = AssetTemplate.create(container="docker", entrypoint="main.cwl", languages=["CWL"])
    template.apply(container="podman")
    template.apply()
    assert template.container == "podman"
    assert template.entrypoint == "main.cwl"
    assert template.languages == ["CWL"]
    template.apply(container=None, entrypoint=None, languages=None)
    assert template.to_dict() == {}
    template.apply(container="docker", entrypoint="new.cwl", languages=["Python"])
    assert template.to_dict() == {
        "application:container": "docker",
        "application:entrypoint": "new.cwl",
        "application:languages": ["Python"],
    }


def test_from_dict_shares_backing_metadata_and_preserves_unknown_members() -> None:
    properties: dict[str, object] = {"custom": {"nested": ["value"]}}
    template = AssetTemplate.from_dict(properties)
    assert template.to_dict() is properties
    template.container = "docker"
    properties["application:entrypoint"] = "main.cwl"
    assert template.entrypoint == "main.cwl"
    assert properties["application:container"] == "docker"
    assert properties["custom"] == {"nested": ["value"]}
    assert "AssetTemplate" in repr(template)


def test_copy_is_independent_at_nested_levels() -> None:
    original = AssetTemplate.create(languages=["CWL"])
    copied = AssetTemplate.from_dict(original.to_dict(), copy=True)
    languages = copied.languages
    assert languages is not None
    languages.append("Python")
    copied.container = "docker"
    assert original.languages == ["CWL"]
    assert original.container is None
    assert copied.to_dict() is not original.to_dict()


@pytest.mark.parametrize("field", ["container", "entrypoint", "languages"])
def test_explicit_null_and_clear_are_distinct(field: str) -> None:
    template = AssetTemplate.create()
    template.set_null(field)
    assert template.to_dict() == {f"application:{field}": None}
    assert getattr(template, field) is None
    template.clear(field)
    template.clear(field)
    assert template.to_dict() == {}


@pytest.mark.parametrize("operation", ["clear", "set_null"])
def test_unknown_member_names_are_rejected(operation: str) -> None:
    template = AssetTemplate.create(container="docker")
    with pytest.raises(KeyError, match="unknown"):
        getattr(template, operation)("unknown")
    assert template.to_dict() == {"application:container": "docker"}
