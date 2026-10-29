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

# Scope, architecture, and validation

## Package structure

The distribution is named `pystac-ext-application`, while the import path is `pystac.extensions.application`. The wheel excludes the shared `pystac.extensions` initializer owned by PySTAC.

`ApplicationExtension.ext()` returns a wrapper bound to an Item, Catalog, Collection, Asset, ItemAssetDefinition, or Link. The wrapper writes directly into the object's metadata dictionary, so serialization uses PySTAC's normal `to_dict()` method. The package stores application metadata; it does not run containers or workflows.

Asset, item asset definition, and Link registration is managed through the owner. Item-owned Assets inherit missing Application fields from Item properties; explicit null masks inherited values. Collection-owned Assets do not inherit Collection fields.

## Nested template values

Catalogs and Collections expose `assetTemplates` as a map and `linkTemplates` as a list. Both contain `AssetTemplate` wrappers. Setters encode wrappers into plain JSON containers. Getters wrap the stored nested dictionaries by reference, so editing a retrieved template changes the owning STAC object's serialized metadata.

`AssetTemplate.from_dict()` also wraps by reference unless `copy=True` is requested. Unknown JSON members survive wrapping. The module is generated: changes to schema-defined fields belong in the source schema and generation workflow.

## Collection summaries

Collections support both direct metadata through `ext()` and summaries through `summaries()`. The summary helper exposes container, entrypoint, and languages. It preserves complete lists, ranges, and JSON Schema dictionaries and replaces the previous representation when a summary is assigned. It does not compute summaries from Items.

## Validation boundaries

Type annotations describe expected values but do not enforce every constraint at runtime. Field access checks target applicability, and template decoding checks the shapes of maps, lists, and nested objects. Reading or writing metadata does not perform full JSON Schema validation.

`apply()` checks all supplied field names and their applicability before changing metadata. Omitted fields are preserved; `None` removes a field. This preflight check does not validate all supplied values or guarantee rollback for arbitrary setter failures. `set_null()` stores explicit JSON null without checking whether the schema permits it.

For full STAC and extension validation, install PySTAC's validation extra with `python -m pip install "pystac[validation]"` and call `item.validate()` or validate the owning STAC object. Validation may retrieve remote schemas, so the referenced schema URLs must be accessible or supplied through an application-configured validator. Neither `apply()` nor `to_dict()` performs JSON Schema validation.

The [field reference](../reference/fields.md) describes supported properties and summaries.

## Schema registration and versions

`SCHEMA_URI` identifies Application v0.1.0. `has_extension()` checks for this exact URI. `ext()` requires registration unless `add_if_missing=True` is supplied; for owned objects, registration is checked or added on the owner. Adding the current URI does not migrate older metadata. The module does not expose migration hooks.
