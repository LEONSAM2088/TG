from dataclasses import dataclass
from utils.db_api.sqlLite import DB


@dataclass
class Item:
    title: str
    price: int
    description: str
    photo_link: str
    metro_station: str
    weight: int
    type: str
    blocked: bool


class ItemEntity:
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
