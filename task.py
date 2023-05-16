from prettytable import PrettyTable


class TaskList:
    def __init__(self) -> None:
        self.tasks = []

    def add(self, task) -> None:
        self.tasks.append(task)

    def pretty_print(self):
        prettyTable = PrettyTable()
        prettyTable.field_names = ["Task", "Name", "Urgency", "Importance"]
        prettyTable.align["Task"] = "r"
        prettyTable.align["Name"] = "l"
        for i, task in enumerate(self.tasks):
            prettyTable.add_row(
                [
                    f"{i}",
                    task.name,
                    "Urgent" if task.urgent else "",
                    "Important" if task.important else "",
                ]
            )
        print(prettyTable)


class Task:
    def __init__(self, name="", urgent=False, important=False) -> None:
        self.name = name
        self.urgent = urgent
        self.important = important

    def __str__(self):
        return (
            "[Name]: {name}\n"
            "{urgency}\n"
            "{importance}".format(
                name=self.name,
                urgency="[Urgent]" if self.urgent else "[Not urgent]",
                importance="[Important]" if self.important else "[Not important]",
            )
        )
