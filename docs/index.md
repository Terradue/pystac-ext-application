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

# Application PySTAC extension

`pystac-ext-application` reads and writes Application extension metadata on PySTAC objects. It exposes container, entrypoint, and language fields, plus asset and link templates on Catalogs and Collections. Import the API from `pystac.extensions.application`.

The implementation declares the schema identifier `https://stac-extensions.github.io/application/v0.1.0/schema.json`. The Python distribution version is independent of the extension specification version.

```bash
python -m pip install pystac-ext-application
```

- [Create an Application Item](tutorials/first-steps.md) and round-trip its metadata.
- [Work with Application metadata](how-to/use-extension.md) on Items, Catalogs, Collections, Assets, item asset definitions, Links, and Collection summaries.
- [Look up fields](reference/fields.md), supported targets, and update semantics.
- [Browse the Python API](reference/api.md).
- [Understand the architecture](explanation/architecture.md) and validation boundaries.
