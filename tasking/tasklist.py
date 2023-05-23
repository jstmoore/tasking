from prettytable import PrettyTable
from task import Task

class TaskList:
    """List of tasks which may be displayed in tabular, readable form.

    Attributes:
        tasks: List of tasks.
    """
    def __init__(self) -> None:
        """Initializes with empty list of tasks."""
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        """Adds task to list of tasks.

        Args:
            task (Task): Task to be added to list of tasks.
        """
        self.tasks.append(task)

    def pretty_print(self):
        """Prints tabular form of list of tasks.

        Configuration is so that the display of each task is an abbreviated
        overview instead of the default task view.

        For each task, we write:
            - Position in list
            - Name
            - Urgent if so
            - Important if so
            - Number of children
        """
        pretty_table = PrettyTable()
        pretty_table.field_names = ["Task", "Name", "Urgency", "Importance", "Children"]
        pretty_table.align["Task"] = "r"
        pretty_table.align["Name"] = "l"
        pretty_table.align["Children"] = "r"
        for i, task in enumerate(self.tasks):
            pretty_table.add_row(
                [
                    f"{i}",
                    task.name,
                    "Urgent" if task.urgent else "",
                    "Important" if task.important else "",
                    len(task.children),
                ]
            )
        print(pretty_table)
