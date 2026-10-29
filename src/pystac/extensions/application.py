# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generated PySTAC extension. Edit the source schema and regenerate to update."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Mapping

from pystac.extensions.base import (
    ExtensionManagementMixin,
    PropertiesExtension,
    SummariesExtension,
)

import pystac

SCHEMA_URI = "https://stac-extensions.github.io/application/v0.1.0/schema.json"
FIELD_TARGETS = {
    "application:container": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "application:entrypoint": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "application:languages": [
        "asset",
        "catalog",
        "collection",
        "item",
        "item_asset",
        "link",
        "summary",
    ],
    "assetTemplates": ["catalog", "collection"],
    "linkTemplates": ["catalog", "collection"],
}
FIELD_NAMES = {
    "container": "application:container",
    "entrypoint": "application:entrypoint",
    "languages": "application:languages",
    "assetTemplates": "assetTemplates",
    "linkTemplates": "linkTemplates",
}
TARGETS = ["asset", "catalog", "collection", "item", "item_asset", "link", "summary"]
T = TypeVar(
    "T",
    bound="pystac.Collection | pystac.Catalog | pystac.Item | pystac.Asset | pystac.ItemAssetDefinition | pystac.Link",
)


def _target_for(obj: object) -> str:
    """Identify supported STAC targets, checking Collection before its Catalog base."""
    target_types = (
        (pystac.Collection, "collection"),
        (pystac.Catalog, "catalog"),
        (pystac.Item, "item"),
        (pystac.Asset, "asset"),
        (pystac.ItemAssetDefinition, "item_asset"),
        (pystac.Link, "link"),
    )
    for object_type, target in target_types:
        if isinstance(obj, object_type):
            if target not in TARGETS:
                break
            return target
    raise pystac.ExtensionTypeError(f"Unsupported extension target: {type(obj).__name__}")


class _Unset:
    """Distinguish omitted arguments from explicit JSON null."""


_UNSET = _Unset()


def _encode(value: Any) -> Any:
    """Convert generated objects at any depth into plain JSON containers."""
    if isinstance(value, _Object):
        value = value.properties
    if isinstance(value, dict):
        return {key: _encode(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(child) for child in value]
    return value


def _decode(value: Any, codec: Any) -> Any:
    """Wrap schema-declared objects while retaining live backing dictionaries."""
    if value is None or codec is None:
        return value
    kind, detail = codec
    if kind == "object":
        return _MODELS[detail].from_dict(value)
    if kind == "list":
        return _decode_list(value, detail)
    if kind == "map":
        return _decode_map(value, detail)
    raise ValueError(f"Unknown conversion: {kind}")


def _decode_list(value: Any, codec: Any) -> list[Any]:
    """Decode the elements of a schema-declared array."""
    if not isinstance(value, list):
        raise TypeError("Expected a JSON array")
    return [_decode(child, codec) for child in value]


def _decode_map(value: Any, codec: Any) -> dict[str, Any]:
    """Decode the values of a schema-declared object map."""
    if not isinstance(value, dict):
        raise TypeError("Expected a JSON object map")
    return {key: _decode(child, codec) for key, child in value.items()}


_O = TypeVar("_O", bound="_Object")


@dataclass
class _Object:
    """Live wrapper around JSON, following PySTAC value-object conventions."""

    _members: ClassVar[dict[str, str]] = {}
    properties: dict[str, Any]

    def __post_init__(self) -> None:
        """Require a JSON object as the live backing value."""
        if not isinstance(self.properties, dict):
            raise TypeError(f"{type(self).__name__} requires a dictionary")

    @classmethod
    def from_dict(cls: type[_O], properties: dict[str, Any], *, copy: bool = False) -> _O:
        """Wrap by reference, or request an independent copy."""
        from copy import deepcopy

        return cls(deepcopy(properties) if copy else properties)

    def to_dict(self) -> dict[str, Any]:
        """Return the live backing JSON dictionary, as PySTAC Render does."""
        return self.properties

    def _apply(self, values: Mapping[str, object]) -> None:
        """Check update names before changing the backing dictionary."""
        unknown = values.keys() - self._members.keys()
        if unknown:
            raise TypeError(f"Unknown fields: {sorted(unknown)}")
        for name, value in values.items():
            if not isinstance(value, _Unset):
                setattr(self, name, value)

    def clear(self, name: str) -> None:
        """Remove a member using its Python attribute name."""
        self.properties.pop(self._members[name], None)

    def set_null(self, name: str) -> None:
        """Store explicit JSON null using a Python member name."""
        self.properties[self._members[name]] = None

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.properties!r}>"


class AssetTemplate(_Object):
    """Generated nested value object; unknown JSON members are preserved."""

    _members: ClassVar[dict[str, str]] = {
        "container": "application:container",
        "entrypoint": "application:entrypoint",
        "languages": "application:languages",
    }

    @classmethod
    def create(
        cls,
        *,
        container: str | _Unset = _UNSET,
        entrypoint: str | _Unset = _UNSET,
        languages: list[str] | _Unset = _UNSET,
    ) -> AssetTemplate:
        """Create with typed members; omitted optionals are not written.

        Explicit None writes null. Validate the STAC object to check value constraints.
        """
        _values = {
            "application:container": container,
            "application:entrypoint": entrypoint,
            "application:languages": languages,
        }
        return cls(
            {key: _encode(value) for key, value in _values.items() if not isinstance(value, _Unset)}
        )

    def apply(
        self,
        *,
        container: str | _Unset | None = _UNSET,
        entrypoint: str | _Unset | None = _UNSET,
        languages: list[str] | _Unset | None = _UNSET,
    ) -> None:
        """Update supplied members; omitted values are preserved and None removes."""
        self._apply(
            {
                "container": container,
                "entrypoint": entrypoint,
                "languages": languages,
            }
        )

    @property
    def container(self) -> str | None:
        "application:container"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("str | None", self.properties.get("application:container"))

    @container.setter
    def container(self, value: str | None) -> None:
        if value is None:
            self.properties.pop("application:container", None)
        else:
            self.properties["application:container"] = _encode(value)

    @property
    def entrypoint(self) -> str | None:
        "application:entrypoint"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("str | None", self.properties.get("application:entrypoint"))

    @entrypoint.setter
    def entrypoint(self, value: str | None) -> None:
        if value is None:
            self.properties.pop("application:entrypoint", None)
        else:
            self.properties["application:entrypoint"] = _encode(value)

    @property
    def languages(self) -> list[str] | None:
        "application:languages"
        # Schema-derived typing at the unvalidated PySTAC JSON boundary.
        return cast("list[str] | None", self.properties.get("application:languages"))

    @languages.setter
    def languages(self, value: list[str] | None) -> None:
        if value is None:
            self.properties.pop("application:languages", None)
        else:
            self.properties["application:languages"] = _encode(value)


_MODELS: dict[str, type[_Object]] = {
    "AssetTemplate": AssetTemplate,
}


class ApplicationExtension(
    PropertiesExtension,
    ExtensionManagementMixin[pystac.Item | pystac.Collection | pystac.Catalog],
    Generic[T],
):
    """Typed property wrapper; use ext() to check/register the extension.

    Setters preserve JSON representations, including date/time strings and nested
    dictionaries. None removes a property; set_null() explicitly writes JSON null.
    Validate the owning STAC object to enforce full schema constraints.
    """

    def __init__(self, obj: T, target: str) -> None:
        """Bind a schema-supported STAC object's metadata for live updates."""
        self.obj: T = obj
        self._target = target
        self.additional_read_properties: list[dict[str, Any]] | None = None
        if isinstance(obj, (pystac.Item, pystac.ItemAssetDefinition)):
            self.properties = obj.properties
        else:
            self.properties = obj.extra_fields
        if isinstance(obj, pystac.Asset) and isinstance(obj.owner, pystac.Item):
            self.additional_read_properties = [obj.owner.properties]

    @classmethod
    def get_schema_uri(cls) -> str:
        """The canonical schema identifier used for extension registration."""
        return SCHEMA_URI

    @classmethod
    def has_extension(cls, obj: pystac.STACObject) -> bool:
        """Check this exact schema version; migrations are not generated."""
        return SCHEMA_URI in (obj.stac_extensions or [])

    @classmethod
    def ext(cls, obj: T, add_if_missing: bool = False) -> ApplicationExtension[T]:
        """Wrap a schema-supported object and optionally register its extension."""
        target = _target_for(obj)
        if isinstance(obj, (pystac.Asset, pystac.ItemAssetDefinition, pystac.Link)):
            cls.ensure_owner_has_extension(obj, add_if_missing)
        else:
            cls.ensure_has_extension(obj, add_if_missing)
        return cls(obj, target)

    def _check_field(self, key: str) -> None:
        if self._target not in FIELD_TARGETS[key]:
            raise pystac.ExtensionTypeError(f"{key} does not apply to {self._target}")

    def clear(self, name: str) -> None:
        """Remove a field using its generated Python attribute name."""
        key = FIELD_NAMES[name]
        self._check_field(key)
        self.properties.pop(key, None)

    def set_null(self, name: str) -> None:
        """Write explicit JSON null; schema validation checks whether it is permitted."""
        key = FIELD_NAMES[name]
        self._check_field(key)
        self._set_property(key, None, pop_if_none=False)

    def apply(self, **values: Any) -> None:
        """Update only supplied fields; omitted fields are preserved.

        Keys are generated Python attribute names. Unknown or inapplicable fields
        are rejected before mutation. Validate the STAC object to check values afterwards.
        """
        for name in values:
            if name not in FIELD_NAMES:
                raise TypeError(f"Unknown extension field: {name}")
            self._check_field(FIELD_NAMES[name])
        for name, value in values.items():
            setattr(self, name, value)

    @property
    def container(self) -> str | None:
        "application:container"
        self._check_field("application:container")
        if "application:container" in self.properties:
            return cast("str | None", self.properties["application:container"])
        return cast("str | None", self._get_property("application:container", object))

    @container.setter
    def container(self, value: str | None) -> None:
        self._check_field("application:container")
        self._set_property("application:container", _encode(value))

    @property
    def entrypoint(self) -> str | None:
        "application:entrypoint"
        self._check_field("application:entrypoint")
        if "application:entrypoint" in self.properties:
            return cast("str | None", self.properties["application:entrypoint"])
        return cast("str | None", self._get_property("application:entrypoint", object))

    @entrypoint.setter
    def entrypoint(self, value: str | None) -> None:
        self._check_field("application:entrypoint")
        self._set_property("application:entrypoint", _encode(value))

    @property
    def languages(self) -> list[str] | None:
        "application:languages"
        self._check_field("application:languages")
        if "application:languages" in self.properties:
            return cast("list[str] | None", self.properties["application:languages"])
        return cast("list[str] | None", self._get_property("application:languages", object))

    @languages.setter
    def languages(self, value: list[str] | None) -> None:
        self._check_field("application:languages")
        self._set_property("application:languages", _encode(value))

    @property
    def assetTemplates(self) -> dict[str, AssetTemplate] | None:
        "assetTemplates"
        self._check_field("assetTemplates")
        if "assetTemplates" in self.properties:
            return cast(
                "dict[str, AssetTemplate] | None",
                _decode(self.properties["assetTemplates"], ["map", ["object", "AssetTemplate"]]),
            )
        return cast(
            "dict[str, AssetTemplate] | None",
            _decode(
                self._get_property("assetTemplates", object), ["map", ["object", "AssetTemplate"]]
            ),
        )

    @assetTemplates.setter
    def assetTemplates(self, value: dict[str, AssetTemplate] | None) -> None:
        self._check_field("assetTemplates")
        self._set_property("assetTemplates", _encode(value))

    @property
    def linkTemplates(self) -> list[AssetTemplate] | None:
        "linkTemplates"
        self._check_field("linkTemplates")
        if "linkTemplates" in self.properties:
            return cast(
                "list[AssetTemplate] | None",
                _decode(self.properties["linkTemplates"], ["list", ["object", "AssetTemplate"]]),
            )
        return cast(
            "list[AssetTemplate] | None",
            _decode(
                self._get_property("linkTemplates", object), ["list", ["object", "AssetTemplate"]]
            ),
        )

    @linkTemplates.setter
    def linkTemplates(self, value: list[AssetTemplate] | None) -> None:
        self._check_field("linkTemplates")
        self._set_property("linkTemplates", _encode(value))

    @classmethod
    def summaries(
        cls, obj: pystac.Collection, add_if_missing: bool = False
    ) -> SummariesApplicationExtension:
        """Wrap schema-declared Collection summaries and optionally register the extension."""
        if not isinstance(obj, pystac.Collection):
            raise pystac.ExtensionTypeError("Summaries require a Collection")
        cls.ensure_has_extension(obj, add_if_missing)
        return SummariesApplicationExtension(obj)


class SummariesApplicationExtension(SummariesExtension):
    """Collection summaries; ranges, lists and JSON Schema objects are preserved."""

    @property
    def container(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("application:container")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("application:container")
        return value

    @container.setter
    def container(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("application:container")
        self._set_summary("application:container", value)

    @property
    def entrypoint(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("application:entrypoint")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("application:entrypoint")
        return value

    @entrypoint.setter
    def entrypoint(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("application:entrypoint")
        self._set_summary("application:entrypoint", value)

    @property
    def languages(self) -> list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None:
        value = self.summaries.to_dict().get("application:languages")
        if isinstance(value, dict) and "minimum" in value and "maximum" in value:
            return self.summaries.get_range("application:languages")
        return value

    @languages.setter
    def languages(
        self, value: list[Any] | pystac.RangeSummary[Any] | dict[str, Any] | None
    ) -> None:
        self.summaries.remove("application:languages")
        self._set_summary("application:languages", value)
