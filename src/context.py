import abc
import datetime
import json
from typing import Self
from console import Console
from note import Note
from utils.singleton import Singleton


class Context(metaclass=Singleton):
    def __init__(
        self,
        filepath: str,
        states: dict[type["BaseState"], "BaseState"],
        actions: tuple[type["BaseAction"]],
        init_state: type["BaseState"],
        console: Console = Console,
    ) -> None:
        self.__filepath: str = filepath
        self.__states: dict[type[BaseState], BaseState] = states
        self.__actions: tuple[type[BaseAction]] = actions
        self.__current_state: type[BaseState] = init_state
        self.__console: Console = console
        self.__strategy: BaseAction
        self.__data: tuple[Note]

    def get_data_json_type(self) -> dict[int, dict[str, str]]:
        notes_in_dict: dict[int, dict[str, str]] = {}
        note: Note
        for note in self.__data:
            notes_in_dict[note.get_id()] = {
                "name": note.get_name(),
                "text": note.get_text(),
                "date": str(note.get_date()),
            }

        return notes_in_dict

    def set_state(self, new_state: type["BaseState"]) -> None:
        self.__current_state = new_state

    def go_next(self) -> None:
        self.__states[self.__current_state].go_next(self)

    def set_data(self, new_data: list[Note]) -> None:
        self.__data = new_data

    def get_actions(self) -> tuple[type["BaseAction"]]:
        return self.__actions

    def get_current_state(self) -> type["BaseState"]:
        return self.__current_state

    def get_console(self) -> Console:
        return self.__console

    def get_filepath(self) -> str:
        return self.__filepath

    def update_data(self, new_note: Note) -> None:
        self.__data = tuple(list(self.__data) + [new_note])

    def set_strategy(self, strategy: "BaseAction") -> None:
        self.__strategy = strategy

    def execute_strategy(self, **kwargs: list[str] | str | int | datetime.datetime | Self) -> tuple[str] | None:
        return self.__strategy.execute(self=self, data={note.get_id(): note for note in self.__data}, **kwargs)


class BaseState(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def go_next(context: Context) -> None:
        pass


class ConsoleWorkState(BaseState):
    @staticmethod
    def get_name() -> str:
        return "ConsoleWorkState"

    @staticmethod
    def go_next(context: Context) -> None:
        console: Console = context.get_console()
        strategies: dict[str, type[BaseAction]] = ConsoleWorkState.get_strategies_and_menu_dict(context.get_actions())

        menu: str = "\n".join(f"{i} {action.get_name()}" for i, action in strategies.items()) + "\n"
        user_command: str = console.get_command(menu)
        while user_command != "0":
            selected_strategy: BaseAction = strategies[user_command]
            context.set_strategy(selected_strategy)

            if issubclass(selected_strategy, BaseWatchAction):
                console.print_data(context.execute_strategy())
            elif issubclass(selected_strategy, SearchByIdAction):
                console.print_data(context.execute_strategy(id=console.get_number_param()))
            elif issubclass(selected_strategy, SearchByNameAction):
                console.print_data(context.execute_strategy(name=console.get_name_param()))
            elif issubclass(selected_strategy, SearchByDateAction):
                console.print_data(context.execute_strategy(date=console.get_date_param()))
            elif issubclass(selected_strategy, SearchByKeywordsAction):
                console.print_data(context.execute_strategy(keywords=console.get_keywords_param()))
            elif issubclass(selected_strategy, BaseCreateAction):
                context.execute_strategy(
                    name=console.get_note_name(),
                    text=console.get_note_text(),
                    date=console.get_note_creation_time(),
                    context=context,
                )

            user_command = console.get_command(menu)

        context.set_state(SaveDataState)

    @staticmethod
    def get_strategies_and_menu_dict(actions: tuple[type["BaseAction"]]) -> dict[str, type["BaseAction"]]:
        return {str(i + 1): actions[i] for i in range(len(actions))}


class FileWorkState(BaseState):
    @staticmethod
    def get_name() -> str:
        return "FileWorkState"


class ReadDataState(FileWorkState):
    @staticmethod
    def get_name() -> str:
        return "ReadDataState"

    @staticmethod
    def go_next(context: Context) -> None:
        with open(context.get_filepath(), "r", encoding="UTF-8") as file:
            json_data: dict[str, dict[str, str]] = json.load(file)
            # TODO: Add promt to date
            context.set_data(
                tuple(
                    Note(data["name"], data["text"], datetime.datetime.fromisoformat(data["date"]))
                    for data in json_data.values()
                )
            )
        context.set_state(ConsoleWorkState)


class SaveDataState(FileWorkState):
    @staticmethod
    def get_name() -> str:
        return "SaveDataState"

    @staticmethod
    def go_next(context: Context) -> None:
        with open(context.get_filepath(), "w", encoding="UTF-8") as file:
            json.dump(context.get_data_json_type(), file, ensure_ascii=False, indent=4)
        context.set_state(EndState)


class EndState(BaseState):
    pass


class BaseAction(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_name(self) -> str:
        pass


class BaseWatchAction(BaseAction):
    @abc.abstractmethod
    def execute(self, data: dict[int, Note]) -> list[str]:
        pass


class BaseSearchAction(BaseAction):
    @abc.abstractmethod
    def execute(self, data: dict[int, Note], **kwargs: str | list[str] | int | datetime.datetime) -> tuple[str]:
        pass


class BaseCreateAction(BaseAction):
    @abc.abstractmethod
    def execute(self, context: Context, **kwargs: str | datetime.datetime) -> None:
        pass


class WatchAllAction(BaseWatchAction):
    @classmethod
    def get_name(cls) -> str:
        return "Просмотреть все"

    def execute(self, data: dict[int, Note]) -> tuple[str]:
        return tuple(map(str, data.values()))


class WatchNamesAction(BaseWatchAction):
    @classmethod
    def get_name(cls) -> str:
        return "Просмотреть имена"

    def execute(self, data: dict[int, Note]) -> tuple[str]:
        return tuple(map(lambda note: note.get_name(), data.values()))


class SearchByIdAction(BaseSearchAction):
    @classmethod
    def get_name(cls) -> str:
        return "Найти по номеру"

    def execute(self, data: dict[int, Note], **kwargs: str | list[str] | int | datetime.datetime) -> tuple[str]:
        return [data[kwargs["id"]]]


class SearchByNameAction(BaseSearchAction):
    @classmethod
    def get_name(cls) -> str:
        return "Найти по имени"

    def execute(self, data: dict[int, Note], **kwargs: str | list[str] | int | datetime.datetime) -> tuple[str]:
        return tuple(filter(lambda note: note.get_name() == kwargs["name"], data.values()))


class SearchByDateAction(BaseSearchAction):
    @classmethod
    def get_name(cls) -> str:
        return "Найти по дате"

    def execute(self, data: dict[int, Note], **kwargs: str | list[str] | int | datetime.datetime) -> tuple[str]:
        print(kwargs["date"])
        return tuple(filter(lambda note: note.get_date().date() == kwargs["date"], data.values()))


class SearchByKeywordsAction(BaseSearchAction):
    @classmethod
    def get_name(cls) -> str:
        return "Найти по ключевым словам"

    def execute(self, data: dict[int, Note], **kwargs: str | list[str] | int | datetime.datetime) -> tuple[str]:
        return tuple(
            filter(lambda note: any(word in kwargs["keywords"] for word in note.get_text().split()), data.values())
        )


class CreateAction(BaseCreateAction):
    @classmethod
    def get_name(cls) -> str:
        return "Создать заметку"

    def execute(self, **kwargs: str | datetime.datetime | Context) -> None:
        kwargs["context"].update_data(Note(kwargs["name"], kwargs["text"], kwargs["date"]))
