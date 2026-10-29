from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

import pystac
from pystac.extensions.application import SCHEMA_URI, ApplicationExtension, AssetTemplate

if TYPE_CHECKING:
    from collections.abc import Callable

Target = (
    pystac.Item
    | pystac.Collection
    | pystac.Catalog
    | pystac.Asset
    | pystac.ItemAssetDefinition
    | pystac.Link
)


@pytest.fixture(params=["item", "collection", "catalog", "asset", "item_asset", "link"])
def target(
    request: pytest.FixtureRequest, item: pystac.Item, collection: pystac.Collection
) -> Target:
    if request.param == "item":
        return item
    if request.param == "collection":
        return collection
    if request.param == "catalog":
        return pystac.Catalog("catalog", "Application catalog")
    if request.param == "asset":
        asset = pystac.Asset("https://example.org/application.cwl")
        item.add_asset("application", asset)
        return asset
    if request.param == "item_asset":
        collection.item_assets = {"application": pystac.ItemAssetDefinition({})}
        return collection.item_assets["application"]
    link = pystac.Link("related", "https://example.org/application.json")
    item.add_link(link)
    return link


def test_registration_is_required_and_idempotent(target: Target) -> None:
    owner = (
        target.owner
        if isinstance(target, (pystac.Asset, pystac.ItemAssetDefinition, pystac.Link))
        else target
    )
    assert isinstance(owner, pystac.STACObject)
    assert not ApplicationExtension.has_extension(owner)
    with pytest.raises(pystac.ExtensionNotImplemented):
        ApplicationExtension.ext(target)
    extension = ApplicationExtension.ext(target, add_if_missing=True)
    assert extension.obj is target
    ApplicationExtension.ext(target, add_if_missing=True)
    assert owner.stac_extensions == [SCHEMA_URI]
    assert ApplicationExtension.has_extension(owner)
    assert ApplicationExtension.get_schema_uri() == SCHEMA_URI


@pytest.mark.parametrize(
    "field,value", [("container", "docker"), ("entrypoint", "main.cwl"), ("languages", ["CWL"])]
)
def test_fields_update_live_metadata(target: Target, field: str, value: str | list[str]) -> None:
    extension = ApplicationExtension.ext(target, add_if_missing=True)
    properties = (
        target.properties
        if isinstance(target, (pystac.Item, pystac.ItemAssetDefinition))
        else target.extra_fields
    )
    key = f"application:{field}"
    assert getattr(extension, field) is None
    setattr(extension, field, value)
    assert getattr(extension, field) == value
    assert properties[key] == value
    extension.set_null(field)
    assert key in properties and properties[key] is None
    assert getattr(extension, field) is None
    extension.clear(field)
    extension.clear(field)
    assert key not in properties
    setattr(extension, field, value)
    setattr(extension, field, None)
    assert key not in properties


def test_apply_preserves_omitted_fields_and_rejects_unknown_names_atomically(
    item: pystac.Item,
) -> None:
    extension = ApplicationExtension.ext(item, add_if_missing=True)
    extension.apply(container="docker", entrypoint="main.cwl", languages=["CWL"])
    extension.apply(container="podman", entrypoint=None)
    extension.apply()
    assert extension.container == "podman"
    assert extension.entrypoint is None
    assert extension.languages == ["CWL"]
    with pytest.raises(TypeError, match="Unknown extension field: typo"):
        extension.apply(container="changed", typo="invalid")
    assert extension.container == "podman"


@pytest.mark.parametrize("field", ["assetTemplates", "linkTemplates"])
def test_item_rejects_template_operations_without_mutation(item: pystac.Item, field: str) -> None:
    extension = ApplicationExtension.ext(item, add_if_missing=True)
    extension.container = "docker"
    operations: list[Callable[[], object]] = [
        lambda: getattr(extension, field),
        lambda: setattr(extension, field, None),
        lambda: extension.clear(field),
        lambda: extension.set_null(field),
        lambda: extension.apply(container="changed", **{field: None}),
    ]
    for operation in operations:
        with pytest.raises(pystac.ExtensionTypeError, match=f"{field} does not apply to item"):
            operation()
    assert extension.container == "docker"
    assert field not in item.properties


@pytest.mark.parametrize(
    "field,value", [("container", "docker"), ("entrypoint", "main.cwl"), ("languages", ["CWL"])]
)
def test_asset_inherits_item_values_unless_explicitly_overridden(
    item: pystac.Item, field: str, value: str | list[str]
) -> None:
    parent = ApplicationExtension.ext(item, add_if_missing=True)
    setattr(parent, field, value)
    asset = pystac.Asset("application.cwl")
    item.add_asset("application", asset)
    extension = ApplicationExtension.ext(asset)
    assert getattr(extension, field) == value
    extension.set_null(field)
    assert getattr(extension, field) is None
    extension.clear(field)
    assert getattr(extension, field) == value
    override = ["Python"] if isinstance(value, list) else "override"
    setattr(extension, field, override)
    assert getattr(extension, field) == override
    assert getattr(parent, field) == value
    setattr(extension, field, None)
    assert getattr(extension, field) == value


@pytest.mark.parametrize("kind", ["catalog", "collection"])
def test_templates_serialize_and_decode_as_live_wrappers(
    collection: pystac.Collection, kind: str
) -> None:
    owner = collection if kind == "collection" else pystac.Catalog("catalog", "Applications")
    extension = ApplicationExtension.ext(owner, add_if_missing=True)
    assert extension.assetTemplates is None
    assert extension.linkTemplates is None
    template = AssetTemplate.create(container="docker", entrypoint="main.cwl", languages=["CWL"])
    extension.assetTemplates = {"workflow": template}
    extension.linkTemplates = [template]
    serialized = json.loads(json.dumps(owner.to_dict()))
    assert serialized["assetTemplates"] == {"workflow": template.to_dict()}
    assert serialized["linkTemplates"] == [template.to_dict()]
    assets = extension.assetTemplates
    links = extension.linkTemplates
    assert assets is not None and links is not None
    assets["workflow"].container = "podman"
    links[0].entrypoint = "other.cwl"
    assert owner.extra_fields["assetTemplates"]["workflow"]["application:container"] == "podman"
    assert owner.extra_fields["linkTemplates"][0]["application:entrypoint"] == "other.cwl"
    assert template.container == "docker"
    assert template.entrypoint == "main.cwl"
    extension.assetTemplates = None
    extension.linkTemplates = None
    assert "assetTemplates" not in owner.extra_fields
    assert "linkTemplates" not in owner.extra_fields


@pytest.mark.parametrize(
    "field,value,message",
    [
        ("assetTemplates", [], "Expected a JSON object map"),
        ("linkTemplates", {}, "Expected a JSON array"),
        ("assetTemplates", {"bad": "invalid"}, "requires a dictionary"),
        ("linkTemplates", ["invalid"], "requires a dictionary"),
    ],
)
def test_malformed_template_metadata_is_rejected(
    collection: pystac.Collection, field: str, value: object, message: str
) -> None:
    extension = ApplicationExtension.ext(collection, add_if_missing=True)
    collection.extra_fields[field] = value
    with pytest.raises(TypeError, match=message):
        getattr(extension, field)


def test_item_round_trip_preserves_application_metadata(item: pystac.Item) -> None:
    extension = ApplicationExtension.ext(item, add_if_missing=True)
    extension.apply(container="docker", entrypoint="main.cwl", languages=["CWL"])
    restored = pystac.Item.from_dict(json.loads(json.dumps(item.to_dict())))
    restored_extension = ApplicationExtension.ext(restored)
    assert restored_extension.container == "docker"
    assert restored_extension.entrypoint == "main.cwl"
    assert restored_extension.languages == ["CWL"]


@pytest.mark.parametrize("add_if_missing", [False, True])
def test_unowned_assets_require_an_owner_for_registration(add_if_missing: bool) -> None:
    asset = pystac.Asset("application.cwl")
    if add_if_missing:
        with pytest.raises(pystac.STACError, match="owner"):
            ApplicationExtension.ext(asset, add_if_missing=True)
    else:
        extension = ApplicationExtension.ext(asset)
        extension.container = "docker"
        assert asset.extra_fields["application:container"] == "docker"


def test_different_schema_version_does_not_count_as_registered(item: pystac.Item) -> None:
    previous_schema = "https://stac-extensions.github.io/application/v0.0.1/schema.json"
    item.stac_extensions = [previous_schema]
    assert not ApplicationExtension.has_extension(item)
    with pytest.raises(pystac.ExtensionNotImplemented):
        ApplicationExtension.ext(item)
    ApplicationExtension.ext(item, add_if_missing=True)
    assert item.stac_extensions == [previous_schema, SCHEMA_URI]


def test_collection_assets_do_not_inherit_collection_fields(collection: pystac.Collection) -> None:
    parent = ApplicationExtension.ext(collection, add_if_missing=True)
    parent.container = "docker"
    asset = pystac.Asset("application.cwl")
    collection.add_asset("application", asset)
    extension = ApplicationExtension.ext(asset)
    assert extension.container is None
    extension.container = "podman"
    assert parent.container == "docker"


@pytest.mark.parametrize("field", ["assetTemplates", "linkTemplates"])
def test_explicit_null_templates_are_preserved(collection: pystac.Collection, field: str) -> None:
    extension = ApplicationExtension.ext(collection, add_if_missing=True)
    extension.set_null(field)
    assert field in collection.extra_fields
    assert getattr(extension, field) is None
    extension.clear(field)
    assert field not in collection.extra_fields
