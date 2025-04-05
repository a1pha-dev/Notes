import datetime


class Note:
    __id: int = 0

    def __init__(self, name: str, text: str, date: datetime.datetime) -> None:
        self.__id: int = self.auto_increment()
        self.__name: str = name
        self.__text: str = text
        self.__date: datetime.datetime = date

    @classmethod
    def auto_increment(cls) -> int:
        cls.__id += 1
        return cls.__id

    @classmethod
    def set_last_id(cls, init_id: int) -> None:
        cls.__id = init_id

    def get_name(self) -> str:
        return self.__name

    def get_text(self) -> str:
        return self.__text

    def get_date(self) -> str:
        return self.__date
