import abc
import datetime

from note import Note


class BaseWatchAction(abc.ABC):
    @abc.abstractmethod
    def execute(self, data: dict[int, Note]) -> list[str]:
        pass


class BaseSearchAction(abc.ABC):
    @abc.abstractmethod
    def execute(self, data: dict[int, Note], **kwargs: list[str] | int | datetime.datetime) -> tuple[str]:
        pass


class WatchAllAction(BaseWatchAction):
    def execute(self, data: dict[int, Note]) -> tuple[str]:
        return tuple(map(str, data.values()))


class WatchNamesAction(BaseWatchAction):
    def execute(self, data: dict[int, Note]) -> tuple[str]:
        return tuple(map(lambda note: note.get_name(), data.values()))


class SearchById(BaseSearchAction):
    def execute(self, data: dict[int, Note], **kwargs: list[str] | int | datetime.datetime) -> tuple[str]:
        return [data[kwargs["id"]]]


class SearchByName(BaseSearchAction):
    def execute(self, data: dict[int, Note], **kwargs: list[str] | int | datetime.datetime) -> tuple[str]:
        return tuple(filter(lambda note: note.get_name() == kwargs["name"], data.values()))


class SearchByDate(BaseSearchAction):
    def execute(self, data: dict[int, Note], **kwargs: list[str] | int | datetime.datetime) -> tuple[str]:
        return tuple(filter(lambda note: note.get_date().date == kwargs["date"].date, data.values()))


class SearchByKeywords(BaseSearchAction):
    def execute(self, data: dict[int, Note], **kwargs: list[str] | int | datetime.datetime) -> tuple[str]:
        return tuple(
            filter(lambda note: any(word in kwargs["keywords"] for word in note.get_text().split()), data.values())
        )
