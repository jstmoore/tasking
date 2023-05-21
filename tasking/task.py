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

    def __eq__(self, other):
        # self.children == other.children
        return  self.name == other.name and \
            self.urgent == other.urgent and \
            self.important == other.important and \
            self.description == other.description and \
            len(self.children) == len(other.children) and \
            all(a is b for (a, b) in zip(self.children, other.children))
