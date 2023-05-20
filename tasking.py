from task import Task, TaskList
import argparse
import pickle


def read_tasks():
    try:
        with open("tasks.pkl", "rb") as fin:
            return pickle.load(fin)
    except:
        return []


def write_tasks(tasks):
    with open("tasks.pkl", "wb") as fout:
        pickle.dump(tasks, fout)


def add_task(args):
    name = args.name
    desc = args.desc
    urgency = args.urgent
    importance = args.important

    tasks = read_tasks()

    task = Task(name, desc, urgency, importance)
    tasks.append(task)

    write_tasks(tasks)


def modify_task(args):
    pass


def print_task(args):
    pass


def print_all_tasks(args):
    tasks = read_tasks()

    task_list = TaskList()
    task_list.tasks = tasks

    task_list.pretty_print()


def make_parser():
    parser = argparse.ArgumentParser(description="Tasking -- Task management tool")

    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

    add_parser = subparsers.add_parser(
        "add",
        help="Add a task",
        aliases=[
            "a",
        ],
    )
    add_parser.add_argument("name", help="Name of task", default="", nargs="?")
    add_parser.add_argument(
        "-D", "-d", "--desc", help="Description of task", default=""
    )
    add_parser.add_argument(
        "-U", "-u", "--urgent", help="Urgency of task", action="store_true"
    )
    add_parser.add_argument(
        "-I", "-i", "--important", help="Importance of task", action="store_true"
    )
    add_parser.set_defaults(func=add_task)

    modify_parser = subparsers.add_parser("modify", help="Modify a task", aliases=["m"])
    modify_parser.add_argument("taskid", help="ID of the task")
    modify_parser.add_argument("-N", "-n", "--name", help="Name of task", default=None)
    modify_parser.add_argument(
        "-D", "-d", "--desc", help="Description of task", default=None
    )
    modify_parser.add_argument(
        "-U", "-u", "--urgent", help="Urgency of task", action="store_true"
    )
    modify_parser.add_argument(
        "-I", "-i", "--important", help="Importance of task", action="store_true"
    )
    modify_parser.set_defaults(func=modify_task)

    print_parser = subparsers.add_parser("print", help="Print a task", aliases=["p"])
    print_parser.add_argument("taskid", help="ID of the task")
    print_parser.add_argument(
        "-S", "-s", help="Prints tabular overview of subtasks", action="store_true"
    )
    print_parser.set_defaults(func=print_task)

    print_all_parser = subparsers.add_parser(
        "printall", help="Print all tasks", aliases=["pa"]
    )
    print_all_parser.set_defaults(func=print_all_tasks)

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    if not args:
        return
    args.func(args)


if __name__ == "__main__":
    main()
