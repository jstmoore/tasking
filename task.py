from prettytable import PrettyTable


class TaskList:
    def __init__(self) -> None:
        self.tasks = []

    def add(self, task) -> None:
        self.tasks.append(task)

    def pretty_print(self):
        prettyTable = PrettyTable()
        prettyTable.field_names = ["Task", "Name", "Urgency", "Importance", "Children"]
        prettyTable.align["Task"] = "r"
        prettyTable.align["Name"] = "l"
        prettyTable.align["Children"] = "r"
        for i, task in enumerate(self.tasks):
            prettyTable.add_row(
                [
                    f"{i}",
                    task.name,
                    "Urgent" if task.urgent else "",
                    "Important" if task.important else "",
                    len(task.children),
                ]
            )
        print(prettyTable)


class Task:
    def __init__(
        self, name="", urgent=False, important=False, description=None, children=None
    ) -> None:
        self.name = name
        self.urgent = urgent
        self.important = important

        if not children:
            children = []
        self.children = children

        self.description = description

    def add(self, child):
        self.children.append(child)

    def __str__(self):
        sb = []

        sb.append(f"[Name]: {self.name}")

        if self.urgent:
            sb.append("\t - Urgent")

        if self.important:
            sb.append("\t - Important")

        if self.description:
            sb.append("[Description]")

            for i in range(0, len(self.description), 80):
                sb.append(f"\t{self.description[i:i + 80]}")

        if self.children:
            sb.append("[Children]")

            for child in self.children:
                sb.append(f"\t - {child.name}")

        return "\n".join(sb)
