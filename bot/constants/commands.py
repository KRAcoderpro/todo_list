from enum import Enum


class UserTaskCommands(str, Enum):
    ADD = "Добавить задачу"
    DELETE = "Удалить задачу"
    LIST_ALL = "Мои задачи"
    CANCEL_CREATE = "Отменить создание задачи"


class UserCategoryCommands(str, Enum):
    ADD = "Добавить категорию"
    DELETE = "Удалить задачу"
    CANCEL_CREATE = "Отменить создание категории"

