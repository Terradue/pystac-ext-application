<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Application fields

`ApplicationExtension.ext()` supports Items, Catalogs, Collections, Assets, item asset definitions, and Links.

| STAC field | Python property | Value type | Supported targets |
| --- | --- | --- | --- |
| `application:container` | `container` | `str` | All supported targets |
| `application:entrypoint` | `entrypoint` | `str` | All supported targets |
| `application:languages` | `languages` | `list[str]` | All supported targets |
| `assetTemplates` | `assetTemplates` | `dict[str, AssetTemplate]` | Catalogs and Collections |
| `linkTemplates` | `linkTemplates` | `list[AssetTemplate]` | Catalogs and Collections |

The template field names have no `application:` prefix. Their Python properties retain the schema's camelCase spelling. `AssetTemplate` exposes the same `container`, `entrypoint`, and `languages` members as the extension, with prefixed keys in its backing dictionary.

## Storage and inheritance

Items and item asset definitions store fields in `properties`. Catalogs, Collections, Assets, and Links use `extra_fields`. Wrappers update these dictionaries directly.

Item-owned Assets fall back to Item properties for missing fields. An explicit Asset null overrides that fallback. Other targets do not inherit metadata from their owners.

## Update semantics

- Getters return `None` for absent fields without an inherited value, or for explicit null.
- Property setters and `apply()` remove fields assigned `None`.
- `apply()` preserves omitted fields, including when called without arguments.
- `set_null(name)` stores explicit JSON null; schema validation determines whether it is allowed.
- `clear(name)` removes a field and does nothing if it is already absent.
- `clear()` and `set_null()` accept Python attribute names and raise `KeyError` for unknown names.
- `apply()` raises `TypeError` for unknown names and `pystac.ExtensionTypeError` for fields unsupported on the target, before applying any updates.
- Accessing or setting template fields on targets other than Catalogs and Collections raises `pystac.ExtensionTypeError`.

## Nested templates

`AssetTemplate.create()` accepts optional typed members and omits unspecified values. `AssetTemplate.apply()` preserves unspecified values and removes members set to `None`. `clear()` and `set_null()` distinguish absence from explicit null.

`AssetTemplate.from_dict(properties)` wraps the dictionary by reference and retains unknown keys. `copy=True` makes a deep copy. `to_dict()` returns the live dictionary. Extension template getters return live nested wrappers; setters encode supplied wrappers into plain JSON containers.

Malformed stored template maps or arrays raise `TypeError` when read. Each nested template must be backed by a dictionary. These structural checks are not full schema validation.

## Collection summaries

`ApplicationExtension.summaries(collection)` exposes `container`, `entrypoint`, and `languages`, mapped to their corresponding `application:` keys.

Each property accepts a list, a `pystac.RangeSummary`, a JSON Schema dictionary, or `None`. Getters return the complete stored summary, converting dictionaries with both `minimum` and `maximum` to a `RangeSummary`. Missing summaries return `None`. Setters replace the previous summary representation; assigning `None` removes it. Whether a summary value is valid for a field is determined by the schema.

The helper does not compute summaries from Items and has no `apply()` method.
