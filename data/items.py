from dataclasses import dataclass
from utils.db_api.sqlLite import DB


@dataclass
class Item:
    title: str
    price: int
    description: str
    photo_link: str
    metro_station: str
    weight: float
    type: str
    blocked: bool


def itemExistTitle(items, o):
    for i in items:
        if i.title == o:
            return True
    return False


def itemExistPrice(items, o):
    for i in items:
        if i.price == o:
            return True
    return False


class ItemEntity:

    @staticmethod
    def getMenuItems():
        data = ItemEntity.getItems()
        items = []
        for item in data:

            if not itemExistTitle(items, item.title) or not itemExistPrice(items, item.price):
                items.append(item)

        return items

    @staticmethod
    def getItems():

        data = DB.select_items()
        Items = []

        for item in data:
            it = Item(
                title=item[1],
                price=item[2],
                description=item[3],
                photo_link=item[4],
                metro_station=item[5],
                weight=item[6],
                type=item[7],
                blocked=item[8]
            )
            if it not in Items and not it.blocked:
                Items.append(it)
        return Items
