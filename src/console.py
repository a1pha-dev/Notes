import datetime
from sys import stdin


class Console:
    @staticmethod
    def get_command(menu: str) -> str:
        # TODO: Add input check
        return input(menu)

    @staticmethod
    def get_keywords_param() -> list[str]:
        return input().split()

    @staticmethod
    def get_number_param() -> int:
        return int(input())

    @staticmethod
    def get_name_param() -> str:
        return input("Введите название заметки: ")

    @staticmethod
    def get_date_param() -> str:
        return datetime.datetime.strptime(input(), "%d.%m.%Y").date()

    @staticmethod
    def get_note_text() -> str:
        print("Введите текст заметки:")
        return stdin.read()

    @staticmethod
    def get_note_name() -> str:
        return input("Введите название заметки: ")

    @staticmethod
    def get_note_creation_time() -> datetime.datetime:
        return datetime.datetime.now()

    @staticmethod
    def print_data(data: list[str]) -> None:
        for note in data:
            print("-" * 20)
            print(note)
