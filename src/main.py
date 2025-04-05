from context import (
    Context,
    ConsoleWorkState,
    EndState,
    ReadDataState,
    SaveDataState,
    CreateAction,
    WatchAllAction,
    WatchNamesAction,
    SearchByIdAction,
    SearchByDateAction,
    SearchByNameAction,
    SearchByKeywordsAction,
)


def main() -> None:
    context: Context = Context(
        "C:\\Users\\a1pha\\PythonProjects\\Notes\\src\\notes.json",
        {ReadDataState: ReadDataState(), ConsoleWorkState: ConsoleWorkState(), SaveDataState: SaveDataState()},
        (
            CreateAction,
            WatchAllAction,
            WatchNamesAction,
            SearchByIdAction,
            SearchByDateAction,
            SearchByNameAction,
            SearchByKeywordsAction,
        ),
        ReadDataState,
    )

    while context.get_current_state() is not EndState:
        context.go_next()


if __name__ == "__main__":
    main()
