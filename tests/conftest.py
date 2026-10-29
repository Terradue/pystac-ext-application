from datetime import datetime, timezone

import pytest

import pystac


@pytest.fixture
def item() -> pystac.Item:
    return pystac.Item(
        id="application-item",
        geometry=None,
        bbox=None,
        datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
        properties={},
    )


@pytest.fixture
def collection() -> pystac.Collection:
    return pystac.Collection(
        id="applications",
        description="Application test collection",
        extent=pystac.Extent(
            pystac.SpatialExtent([-180, -90, 180, 90]),
            pystac.TemporalExtent([None, None]),
        ),
    )
