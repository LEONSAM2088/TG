from data.items import ItemEntity
from utils.db_api.sqlLite import DB


class Metro:

    @staticmethod
    def stations_by_item(item_name):

        stations = []
        for item in ItemEntity.getItems():
            if item.metro_station not in stations and item_name == item.price:
                stations.append(item.metro_station)

        return stations
