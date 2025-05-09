from .create_task import windows as create_task_windows
from .edit_task import windows as edit_task_windows
from .edit_task import getters as edit_task_getter
from .create_catagory import windows as create_category_windows
from .edit_catagory import windows as edit_category_windows
from .show_tasks import windows as show_tasks_windows

from .base import dialog_with_main_menu

create_task_dialog = dialog_with_main_menu(
    create_task_windows.title_window,
    create_task_windows.category_type_window,
    create_task_windows.category_window,
    create_task_windows.due_date_window,
    create_task_windows.due_time_window,
    create_task_windows.confirm_window,
)
edit_task_dialog = dialog_with_main_menu(
    edit_task_windows.title_window,
    edit_task_windows.category_type_window,
    edit_task_windows.category_window,
    edit_task_windows.due_date_window,
    edit_task_windows.due_time_window,
    edit_task_windows.confirm_window,
    on_start=edit_task_getter.set_prev_task_data
)

create_category_dialog = dialog_with_main_menu(
    create_category_windows.name_window,
    create_category_windows.confirm_window,
)

edit_category_dialog = dialog_with_main_menu(
    edit_category_windows.name_window,
    edit_category_windows.confirm_window,
)

show_tasks_dialog = dialog_with_main_menu(
    show_tasks_windows.task_types_window,
    show_tasks_windows.category_type_window,
    show_tasks_windows.by_category_window,
)
