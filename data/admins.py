from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    card: str
    tg_id: int


Admins = [Admin(
    id=0,
    card="0000 0000 1111 2222",
    tg_id=1066208089
)]
