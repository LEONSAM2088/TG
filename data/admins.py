from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    card: str
    tg_id: int


Admins = [
    Admin(
        id=0,
        card="5536 9140 3901 8001",
        tg_id=1836632238
    )
]

# Admin(
#     id=1,
#     card="0000 0000 0000 0000",
#     tg_id=478031178
# )