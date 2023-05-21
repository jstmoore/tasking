from tasking.tasklist import TaskList
from tasking.task import Task
from unittest import TestCase, skip


class TestTaskList(TestCase):
    def test_add_task(self):
        task_list = TaskList()
        task_to_add = Task("test task")

        assert len(task_list.tasks) == 0

        task_list.add(task_to_add)

        assert len(task_list.tasks) == 1
        assert task_list.tasks[0] == task_to_add

    @skip("This test is not yet implemented")
    def test_list_tasks(self):
        pass
