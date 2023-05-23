"""CLI for tasking.

Contains the logic for parsing commands of the form:
tasking:
    - add
        - optionals: [name, --desc, --urgent, --important]
    - modify taskid
        TODO: subtask, design API
        TODO: complete/remove task
    - print taskid
        - optionals: [-S]
    - printall

Parsing is divided into a subparser for each command, associated with a function
for its namespace.
"""

import argparse
import pickle
from task import Task
from tasklist import TaskList


def read_tasks() -> list[Task]:
    """Returns the list of tasks saved in tasks.pkl, or returns an empty list.

    Returns:
        list[Task]: The list of tasks, or an empty list.
    """
    try:
        with open("tasks.pkl", "rb") as fin:
            return pickle.load(fin)
    except FileNotFoundError:
        return []


def write_tasks(tasks: list[Task]):
    """Saves a list of tasks into tasks.pkl.

    Args:
        tasks (list[Task]): List of tasks to be saved into tasks.pkl.
    """
    with open("tasks.pkl", "wb") as fout:
        pickle.dump(tasks, fout)


def add_task(args: argparse.Namespace):
    """Router function to add task into list of tasks in tasks.pkl.

    Args:
        args (Namespace): Returned by parser.arg_parse().
    """
    name = args.name
    desc = args.desc
    urgency = args.urgent
    importance = args.important

    tasks = read_tasks()

    task = Task()
    if name is not None:
        task.name = name
    if desc is not None:
        task.desc = desc

    task.urgent = urgency
    task.important = importance

    tasks.append(task)

    write_tasks(tasks)


def modify_task(args: argparse.Namespace):
    """Router function to modify a task in the list of tasks in tasks.pkl.

    Args:
        args (argparse.Namespace): Returned by parser.arg_parse().
    """
    taskid = args.taskid
    tasks = read_tasks()
    task = tasks[taskid]

    if args.name:
        task.name = args.name
    if args.desc:
        task.description = args.desc
    if args.urgent:
        task.urgent = True
    if args.noturgent:
        task.urgent = False
    if args.important:
        task.important = True
    if args.notimportant:
        task.important = False
    if args.addsubtask is not None:
        task.children.append(tasks[args.addsubtask])
    if args.removesubtask is not None:
        del task.children[args.removesubtask]

    write_tasks(tasks)

    print(args)


def print_task(
    args: argparse.Namespace,
):
    """Router function to print a task in the list of tasks in tasks.pkl.

    Args:
        args (argparse.Namespace): Returned by parser.arg_parse().
    """

    taskid = args.taskid
    tasks = read_tasks()
    print(tasks[taskid])

def print_all_tasks(
    args: argparse.Namespace, #pylint: disable=unused-argument
):
    """Router function to print the tasks in the list of tasks in tasks.pkl.

    Args:
        args (argparse.Namespace): Returned by parser.arg_parse(). Entirely
            used, here.
    """
    tasks = read_tasks()

    task_list = TaskList()
    task_list.tasks = tasks

    task_list.pretty_print()


def make_parser() -> argparse.ArgumentParser:
    """Constructs the main parser for the tasking CLI.

    In the namespace provided, "func" is the function associated with the
    tasking command.

    Returns:
        argparse.ArgumentParser: Parser for tasking CLI.
    """
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
    modify_parser.add_argument("taskid", help="ID of the task", type=int)
    modify_parser.add_argument("-N", "-n", "--name", help="Name of task", default=None)
    modify_parser.add_argument(
        "-D", "-d", "--desc", help="Description of task", default=None
    )
    subtask_group = modify_parser.add_mutually_exclusive_group()
    subtask_group.add_argument(
        "-AS", "-as", "--addsubtask", help="Id of task to add to subtask list", type=int
    )
    subtask_group.add_argument(
        "-RS", "-rs", "--removesubtask", help="Id of task to remove from subtask list", type=int
    )
    urgency_group = modify_parser.add_mutually_exclusive_group()
    importance_group = modify_parser.add_mutually_exclusive_group()
    urgency_group.add_argument(
        "-U", "-u", "--urgent", help="Make task urgent", action="store_true"
    )
    importance_group.add_argument(
        "-I", "-i", "--important", help="Make task important", action="store_true"
    )
    urgency_group.add_argument(
        "-NU", "-nu", "--noturgent", help="Make task not urgent", action="store_true"
    )
    importance_group.add_argument(
        "-NI",
        "-ni",
        "--notimportant",
        help="Make task not important",
        action="store_true",
    )
    modify_parser.set_defaults(func=modify_task)

    print_parser = subparsers.add_parser("print", help="Print a task", aliases=["p"])
    print_parser.add_argument("taskid", help="ID of the task", type=int)
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
    """Runs the CLI.

    The parser is made, and then used to parse user commands. If no commands are
    parsed, we exit.
    Otherwise, we invoke the function stored in args[func] and invoke it on
    the namespace of arguments.
    """
    parser = make_parser()
    args = parser.parse_args()

    if not args:
        return
    args.func(args)


if __name__ == "__main__":
    main()
