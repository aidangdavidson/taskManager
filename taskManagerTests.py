import unittest
from taskManagerDavidson import *


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Set up a new instance of TaskManager for each test
        self.task_manager = TaskManager()

    def test_add_task(self):
        # Test the add_task method
        task = Task("Test Task", datetime.date(2023, 1, 1), 1, "Test Category")
        self.task_manager.add_task(task)
        self.assertIn(task, self.task_manager.priority_queue)

    def test_sort_priority_queue(self):
        # Test the sort_priority_queue method
        task1 = Task("Task 1", datetime.date(2023, 1, 1), 1, "Category A")
        task2 = Task("Task 2", datetime.date(2023, 1, 2), 2, "Category B")
        self.task_manager.priority_queue = [task2, task1]

        # Display the state before sorting
        print("Before sorting:", self.task_manager.priority_queue)

        # Sort the priority queue
        self.task_manager.sort_priority_queue()

        # Display the state after sorting
        print("After sorting:", self.task_manager.priority_queue)

        # Ensure the priority queue is sorted correctly
        self.assertEqual(self.task_manager.priority_queue, [task1, task2])

    def test_display_tasks_to_string(self):
        # Test the display_tasks_to_string method
        task = Task("Test Task", datetime.date(2023, 1, 1), 1, "Test Category")
        self.task_manager.add_task(task)
        tasks_text = self.task_manager.display_tasks_to_string()

        # Ensure that the string representation of the task is present in the output
        self.assertIn(str(task), tasks_text)

    def test_mark_task_complete(self):
        # Test the mark_task_complete method
        task = Task("Test Task", datetime.date(2023, 1, 1), 1, "Test Category")
        self.task_manager.add_task(task)

        # Mark the task as complete and ensure the state is updated
        self.task_manager.mark_task_complete(1)
        self.assertTrue(task.is_complete)


if __name__ == '__main__':
    # Run the unit tests
    unittest.main()
