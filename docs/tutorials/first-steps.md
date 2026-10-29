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

# Create an Application Item

[Install the package](../how-to/install.md) before running this complete example. It creates an Item carrying application metadata and reads that metadata back after serialization.

```python
from datetime import datetime, timezone

import pystac
from pystac.extensions.application import ApplicationExtension

item = pystac.Item(
    id="example-application",
    geometry=None,
    bbox=None,
    datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    properties={"title": "Application example"},
)
application = ApplicationExtension.ext(item, add_if_missing=True)
application.apply(
    container="docker",
    entrypoint="main.cwl",
    languages=["CWL"],
)

serialized = item.to_dict()
assert ApplicationExtension.get_schema_uri() in serialized["stac_extensions"]
assert serialized["properties"]["application:container"] == "docker"
assert serialized["properties"]["application:entrypoint"] == "main.cwl"
assert serialized["properties"]["application:languages"] == ["CWL"]

restored_item = pystac.Item.from_dict(serialized)
restored = ApplicationExtension.ext(restored_item)
assert restored.container == application.container
assert restored.entrypoint == application.entrypoint
assert restored.languages == application.languages
```

`add_if_missing=True` registers the extension schema on the Item. Subsequent calls to `ApplicationExtension.ext(item)` require that registration. The wrapper stores metadata; it does not execute the application.

The core Item `datetime` is supplied by the caller and is independent of the Application fields.

`to_dict()` serializes the Item without running JSON Schema validation. See [validation boundaries](../explanation/architecture.md#validation-boundaries) for the distinction.
