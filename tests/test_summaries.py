import pytest

import pystac
from pystac.extensions.application import SCHEMA_URI, ApplicationExtension


def test_summaries_require_registration(collection: pystac.Collection) -> None:
    with pytest.raises(pystac.ExtensionNotImplemented):
        ApplicationExtension.summaries(collection)
    ApplicationExtension.summaries(collection, add_if_missing=True)
    ApplicationExtension.summaries(collection, add_if_missing=True)
    assert collection.stac_extensions == [SCHEMA_URI]


@pytest.mark.parametrize("field", ["container", "entrypoint", "languages"])
def test_summaries_replace_lists_ranges_and_schemas(
    collection: pystac.Collection, field: str
) -> None:
    extension = ApplicationExtension.summaries(collection, add_if_missing=True)
    key = f"application:{field}"
    assert getattr(extension, field) is None
    setattr(extension, field, ["first", "second"])
    assert getattr(extension, field) == ["first", "second"]
    assert collection.summaries.to_dict()[key] == ["first", "second"]
    setattr(extension, field, pystac.RangeSummary(1, 5))
    summary_range = getattr(extension, field)
    assert isinstance(summary_range, pystac.RangeSummary)
    assert summary_range.to_dict() == {"minimum": 1, "maximum": 5}
    assert key not in collection.summaries.lists
    schema = {"type": "string", "enum": ["docker", "podman"]}
    setattr(extension, field, schema)
    assert getattr(extension, field) == schema
    assert key not in collection.summaries.ranges
    setattr(extension, field, [])
    assert getattr(extension, field) == []
    setattr(extension, field, None)
    assert getattr(extension, field) is None
    assert key not in collection.summaries.to_dict()
