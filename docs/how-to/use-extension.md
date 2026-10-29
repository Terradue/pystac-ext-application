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

# Work with Application metadata

Run the [tutorial](../tutorials/first-steps.md) first. The examples below continue from its `item`, `application`, imports, and timestamp utilities, and can be executed in order.

## Update, remove, or explicitly null a field

```python
application = ApplicationExtension.ext(item)
application.apply(container="podman", entrypoint=None)
assert application.languages == ["CWL"]
assert "application:entrypoint" not in item.properties

application.set_null("entrypoint")
assert item.properties["application:entrypoint"] is None
application.clear("entrypoint")
assert "application:entrypoint" not in item.properties
```

`apply()` preserves omitted fields. Assigning `None` removes a field; `set_null()` stores explicit JSON null, whose validity depends on the schema. `clear()` removes a field using its Python attribute name and is safe to repeat. Unknown or inapplicable names passed to `apply()` are rejected before any fields change.

## Attach asset fields

```python
asset = pystac.Asset(href="https://example.org/main.cwl")
item.add_asset("workflow", asset)
asset_application = ApplicationExtension.ext(asset)
assert asset_application.container == "podman"
asset_application.container = "docker"
assert asset.extra_fields["application:container"] == "docker"
assert application.container == "podman"

asset_application.container = None
assert asset_application.container == "podman"
asset_application.set_null("container")
assert asset_application.container is None
asset_application.clear("container")
assert asset_application.container == "podman"
```

Asset fields are written to `asset.extra_fields`. When an Asset belongs to an Item, absent fields fall back to the Item's properties. Explicit null on the Asset masks the inherited value; clearing the field restores inheritance. Collection-owned Assets do not inherit Collection fields.

Attach Assets, Links, and item asset definitions to their owner before registering the extension. `add_if_missing=True` registers the schema on that owner.

## Set Collection metadata and summaries

```python
collection = pystac.Collection(
    id="example-applications",
    description="Application examples",
    extent=pystac.Extent(
        pystac.SpatialExtent([-180.0, -90.0, 180.0, 90.0]),
        pystac.TemporalExtent([None, None]),
    ),
    license="proprietary",
)
collection_application = ApplicationExtension.ext(collection, add_if_missing=True)
collection_application.container = "docker"

summaries = ApplicationExtension.summaries(collection)
summaries.container = ["docker", "podman"]
summaries.languages = ["CWL", "Python"]
assert summaries.container == ["docker", "podman"]
assert collection.summaries.to_dict()["application:languages"] == ["CWL", "Python"]

summaries.languages = None
assert "application:languages" not in collection.summaries.to_dict()
```

`ext(collection)` accesses Collection metadata; `summaries(collection)` accesses its summaries. Summary setters replace the entire summary for the selected field. Getters preserve full lists, ranges, or JSON Schema objects. The helper exposes `container`, `entrypoint`, and `languages`; it does not aggregate Items or provide an `apply()` method.

## Define asset and link templates

```python
from pystac.extensions.application import AssetTemplate

template = AssetTemplate.create(
    container="docker",
    entrypoint="main.cwl",
    languages=["CWL"],
)
collection_application.assetTemplates = {"workflow": template}
collection_application.linkTemplates = [template]

asset_templates = collection_application.assetTemplates
assert asset_templates is not None
asset_templates["workflow"].entrypoint = "updated.cwl"
assert collection.extra_fields["assetTemplates"]["workflow"]["application:entrypoint"] == "updated.cwl"
assert template.entrypoint == "main.cwl"
```

`assetTemplates` and `linkTemplates` are available only on Catalogs and Collections. Both use `AssetTemplate` values. Setters encode these values into plain JSON dictionaries; getters return wrappers backed by the stored dictionaries, so nested edits are live.

`AssetTemplate.create()` omits unspecified members. `apply()` preserves omitted members and removes those set to `None`. `from_dict()` preserves unknown members and shares the supplied dictionary by default; use `copy=True` for an independent deep copy. `to_dict()` returns the live backing dictionary.

## Use Collection item asset definitions

```python
collection.item_assets = {
    "workflow": pystac.ItemAssetDefinition({"roles": ["data"]}),
}
definition = collection.item_assets["workflow"]
definition_application = ApplicationExtension.ext(definition)
definition_application.entrypoint = "main.cwl"
assert definition.properties["application:entrypoint"] == "main.cwl"
```

Retrieve definitions through `collection.item_assets` so they have an owner. Fields are written to the definition's `properties` dictionary, and extension registration is checked on its Collection.

## Attach Link metadata and use Catalogs

```python
catalog = pystac.Catalog(id="applications", description="Application catalog")
catalog_application = ApplicationExtension.ext(catalog, add_if_missing=True)
catalog_application.languages = ["CWL"]

link = pystac.Link(rel="related", target="https://example.org/application.json")
catalog.add_link(link)
link_application = ApplicationExtension.ext(link)
link_application.entrypoint = "main.cwl"
assert link.extra_fields["application:entrypoint"] == "main.cwl"
```

Catalog metadata uses `catalog.extra_fields`. Link metadata uses `link.extra_fields`, with registration checked on the Link's owner.
