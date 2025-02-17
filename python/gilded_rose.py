# -*- coding: utf-8 -*-


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def clone_items(self) -> list[Item]:
        cloned_items = []
        for item in self.items:
            cloned_items.append(Item(item.name, item.sell_in, item.quality))
        return cloned_items

    def update_quality_passes(self, item):
        # passes logic here
        if item.sell_in < 0:
            item.quality = 0

        if item.sell_in > 10:
            if item.quality < 50:
                item.quality += 1

        elif 5 <= item.sell_in < 11:
            if item.quality < 49:
                item.quality += 2

        elif 0 <= item.sell_in < 5:
            if item.quality < 48:
                item.quality += 3

    def update_sell_in(self, item):
        if item.name != "Sulfuras, Hand of Ragnaros":
            item.sell_in = item.sell_in - 1

    def update_legendary(self, item):
        item.sell_in = item.sell_in
        item.quality = item.quality

    def update_item_quality(self, item):
        """Update item quality according to rules"""

        if item.name.startswith("Backstage passes"):
            self.update_quality_passes(item)

        elif item.name == "Sulfuras, Hand of Ragnaros":
            self.update_legendary(item)

        elif item.name == "Aged Brie":
            if item.quality < 50:
                item.quality += 1

        elif item.name.startswith("Conjured"):
            if item.sell_in > 0:
                item.quality -= 2
            else:
                item.quality -= 4

        else:
            adjustment = -1 if item.sell_in > 0 else -2
            item.quality += adjustment

    def update_quality(self):
        """Update sell-in, quality according to rules"""
        for item in self.items:
            self.update_sell_in(item)
            self.update_item_quality(item)

    # def update_quality(self):
    #     for item in self.items:
    #         if (
    #             item.name != "Aged Brie"
    #             and item.name != "Backstage passes to a TAFKAL80ETC concert"
    #         ):
    #             if item.quality > 0:
    #                 if item.name != "Sulfuras, Hand of Ragnaros":
    #                     item.quality = item.quality - 1
    #         else:
    #             if item.quality < 50:
    #                 item.quality = item.quality + 1
    #                 if item.name == "Backstage passes to a TAFKAL80ETC concert":
    #                     if item.sell_in < 11:
    #                         if item.quality < 50:
    #                             item.quality = item.quality + 1
    #                     if item.sell_in < 6:
    #                         if item.quality < 50:
    #                             item.quality = item.quality + 1

    #         if item.name != "Sulfuras, Hand of Ragnaros":
    #             item.sell_in = item.sell_in - 1

    #         if item.sell_in < 0:
    #             if item.name != "Aged Brie":
    #                 if item.name != "Backstage passes to a TAFKAL80ETC concert":
    #                     if item.quality > 0:
    #                         if item.name != "Sulfuras, Hand of Ragnaros":
    #                             item.quality = item.quality - 1
    #                 else:
    #                     item.quality = item.quality - item.quality
    #             else:
    #                 if item.quality < 50:
    #                     item.quality = item.quality + 1
