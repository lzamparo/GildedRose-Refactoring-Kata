# -*- coding: utf-8 -*-
import pytest
from gilded_rose import Item, GildedRose


# fixtures go here
@pytest.fixture
def items():
    items = [
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
    ]
    return items


@pytest.fixture
def gilded_rose_foo():
    items = [Item("foo", 0, 0)]
    return GildedRose(items)


@pytest.fixture
def gilded_rose_items(items):
    return GildedRose(items)


@pytest.fixture
def gilded_rose_backstage_passes(request):
    items = [
        Item(
            name="Backstage passes to a TAFKAL80ETC concert",
            sell_in=request.param,
            quality=25,
        )
    ]
    return GildedRose(items)


# tests below here
def test_foo(gilded_rose_foo):
    gilded_rose_foo.update_quality()
    assert "foo" == gilded_rose_foo.items[0].name


def test_items_quality_negative(gilded_rose_items):
    gilded_rose_items.update_quality()
    for item in gilded_rose_items.items:
        assert item.quality >= 0


def test_items_quality_max(gilded_rose_items):
    gilded_rose_items.update_quality()
    for item in gilded_rose_items.items:
        if item.name != "Sulfuras, Hand of Ragnaros":
            assert item.quality <= 50


def test_items_quality_degrade(gilded_rose_items):
    # have to clone the items to compare
    # before and after update_quality
    previous_items = gilded_rose_items.clone_items()
    gilded_rose_items.update_quality()
    for old_item, item in zip(previous_items, gilded_rose_items.items):
        if item.name not in (
            "Sulfuras, Hand of Ragnaros",
            "Aged Brie",
            "Backstage passes to a TAFKAL80ETC concert",
        ):
            assert old_item.name == item.name
            assert old_item.quality > item.quality, print(
                f"item: {item.name}, old q: {old_item.quality}, new q: {item.quality}"
            )


def test_items_quality_aged_bree(gilded_rose_items):
    previous_items = gilded_rose_items.clone_items()
    gilded_rose_items.update_quality()
    for old_item, item in zip(previous_items, gilded_rose_items.items):
        if item.name == "Aged Brie":
            assert item.quality > old_item.quality


def test_items_quality_sulfuras(gilded_rose_items):
    previous_items = gilded_rose_items.clone_items()
    gilded_rose_items.update_quality()
    for old_item, item in zip(previous_items, gilded_rose_items.items):
        if item.name == "Sulfuras, Hand of Ragnaros":
            assert old_item.name == item.name
            assert old_item.quality == item.quality


@pytest.mark.parametrize("gilded_rose_backstage_passes", ([10]), indirect=True)
def test_items_quality_backstage_passes_rate(gilded_rose_backstage_passes):
    previous_items = gilded_rose_backstage_passes.clone_items()
    gilded_rose_backstage_passes.update_quality()
    for old_item, item in zip(previous_items, gilded_rose_backstage_passes.items):
        if item.name == "Backstage passes to a TAFKAL80ETC concert":
            assert item.quality == old_item.quality + 2


@pytest.mark.parametrize("gilded_rose_backstage_passes", ([5]), indirect=True)
def test_items_quality_backstage_passes_fastrate(gilded_rose_backstage_passes):
    previous_items = gilded_rose_backstage_passes.clone_items()
    gilded_rose_backstage_passes.update_quality()
    for old_item, item in zip(previous_items, gilded_rose_backstage_passes.items):
        if item.name == "Backstage passes to a TAFKAL80ETC concert":
            assert item.quality == old_item.quality + 3


@pytest.mark.parametrize("gilded_rose_backstage_passes", ([0]), indirect=True)
def test_items_quality_backstage_passes_date(gilded_rose_backstage_passes):
    gilded_rose_backstage_passes.update_quality()
    for item in gilded_rose_backstage_passes.items:
        if item.name == "Backstage passes to a TAFKAL80ETC concert":
            assert item.quality == 0


def test_items_quality_conjured(gilded_rose_items):
    previous_items = gilded_rose_items.clone_items()
    gilded_rose_items.update_quality()
    for old_item, item in zip(previous_items, gilded_rose_items.items):
        if item.name.startswith("Conjured"):
            assert item.name == old_item.name
            assert item.quality == old_item.quality - 2
