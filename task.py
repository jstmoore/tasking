"""Internal data representations of tasks.

Task objects contain all data for itself, and a list of subtasks.

Typical usage example:
    task = Task("Do work")
    task.add(Task("Start work"))

TaskLists maintain a list of Task objects, and may print all tasks in a tabular
format.

Typical usage example:
    task_list = TaskList()
    task_list.add(Task())
    task_list.add(Task())
    task_list.pretty_print()
"""

from prettytable import PrettyTable


class Task:
    """A task with a list of subtasks.

    Attributes:
        Name: String of the task name.
        Urgent: Boolean of if the task is urgent or not.
        Important: Boolean of if the task is important or not.
        Description: String of the task description.
        Subtasks: List of tasks included.
    """
    def __init__(
        self, name="", urgent=False, important=False, description="", subtasks=None
    ) -> None:
        """Initializes a task.

        Args:
            name (str, optional): Task name. Defaults to "".
            urgent (bool, optional): If the task is urgent. Defaults to False.
            important (bool, optional): If the task is important. Defaults to
                False.
            description (str, optional): Task description. Defaults to "".
            subtasks (list[Task], optional): Subtasks. If not passed in, the
                task has an empty list of subtasks. Defaults to None.
        """
        self.name = name
        self.urgent = urgent
        self.important = important

        if not subtasks:
            subtasks = []
        self.children = subtasks

        self.description = description

    def add(self, child: "Task"):
        """Adds a task to the subtasks list.

        Args:
            child (Task): Task to be added to the subtasks list.
        """
        self.children.append(child)

    def __str__(self):
        task_str = []

        task_str.append(f"[Name]: {self.name}")

        if self.urgent:
            task_str.append("\t - Urgent")

        if self.important:
            task_str.append("\t - Important")

        if self.description:
            task_str.append("[Subtasks]")

            for i in range(0, len(self.description), 80):
                task_str.append(f"\t{self.description[i:i + 80]}")

        if self.children:
            task_str.append("[Children]")

            for child in self.children:
                task_str.append(f"\t - {child.name}")

        return "\n".join(task_str)


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
