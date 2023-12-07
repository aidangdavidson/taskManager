import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Node class for linked list
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

# Linked list for managing tasks
class LinkedList:
    def __init__(self):
        self.head = None
        self.logged_messages = []

    def add_task(self, task):
        # Add a new task to end of the list
        new_node = Node(task)
        if not self.head:
            # If the list is empty, set the new node as the head
            self.head = new_node
        else:
            # Traverse the list to find the last node
            current = self.head
            while current.next:
                current = current.next
            # Add the new node to the end of the list
            current.next = new_node

    def display_tasks(self, category=None):
        # Display tasks based on the given category
        current = self.head
        while current:
            if category is None or current.task.category == category:
                task_str = str(current.task)
                self.logged_messages.append(task_str)
            current = current.next

    def mark_task_complete(self, task_index):
        # Mark a task as complete based on the index
        current = self.head
        for _ in range(task_index - 1):
            if current.next is not None:
                current = current.next
            else:
                return "Invalid task index."

        current.task.is_complete = True
        return "Task marked as complete."

# Task class representing the tasks
class Task:
    def __init__(self, description, due_date, priority, category):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.is_complete = False
        self.category = category

    def __lt__(self, other):
        # Compare tasks based on due date and priority
        if self.due_date != other.due_date:
            return self.due_date < other.due_date
        return self.priority < other.priority

    def __str__(self):
        # String representing the task
        status = "Complete" if self.is_complete else "Incomplete"
        return f"Description: {self.description}\nDue Date: {self.due_date}\nPriority: {self.priority}\nCategory: {self.category}\nStatus: {status}\n"

# TaskManager class for managing tasks and the priority queue
class TaskManager:
    def __init__(self):
        self.tasks_linked_list = LinkedList()
        self.priority_queue = []

    # Merge sort for sorting tasks
    def _merge_sort(self, tasks):
        if len(tasks) <= 1:
            return tasks

        # Split the list into two halves
        mid = len(tasks) // 2
        left_half = tasks[:mid]
        right_half = tasks[mid:]

        # Recursively sort each half
        left_half = self._merge_sort(left_half)
        right_half = self._merge_sort(right_half)

        # Merge the sorted halves
        sorted_tasks = []
        left_index = right_index = 0

        while left_index < len(left_half) and right_index < len(right_half):
            if left_half[left_index] < right_half[right_index]:
                sorted_tasks.append(left_half[left_index])
                left_index += 1
            else:
                sorted_tasks.append(right_half[right_index])
                right_index += 1

        # Append the remaining elements from both halves
        sorted_tasks.extend(left_half[left_index:])
        sorted_tasks.extend(right_half[right_index:])

        return sorted_tasks

    def add_task(self, task):
        # Add a task to the linked list and priority queue
        self.tasks_linked_list.add_task(task)
        self.priority_queue.append(task)
        # Sort the priority queue after adding a task
        self.sort_priority_queue()

    def sort_priority_queue(self):
        # Merge Sort implementation for sorting tasks in the priority queue
        self.priority_queue = self._merge_sort(self.priority_queue)

    def display_tasks(self, category=None):
        # Display tasks based on the sorted priority queue
        for task in self.priority_queue:
            if category is None or task.category == category:
                print(task)

    def display_tasks_to_string(self, category=None):
        # Get tasks as a string based on the linked list
        tasks_text = ""
        current = self.tasks_linked_list.head
        while current:
            if category is None or current.task.category == category:
                tasks_text += str(current.task) + "\n"
            current = current.next
        return tasks_text

    def mark_task_complete(self, task_index):
        # Mark a task as complete based on the index
        self.tasks_linked_list.mark_task_complete(task_index)

# TaskAppGUI for the graphical user interface
class TaskAppGUI:
    def __init__(self, master):
        self.task_manager = TaskManager()

        master.title("Task Management App")

        self.label = tk.Label(master, text="Task Management App")
        self.label.pack()

        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack()

        # Entry boxes for task details
        self.description_label = tk.Label(self.menu_frame, text="Enter task description:")
        self.description_label.grid(row=1, column=0)
        self.description_entry = tk.Entry(self.menu_frame)
        self.description_entry.grid(row=1, column=1)

        self.due_date_label = tk.Label(self.menu_frame, text="Enter due date (YYYY-MM-DD):")
        self.due_date_label.grid(row=2, column=0)
        self.due_date_entry = tk.Entry(self.menu_frame)
        self.due_date_entry.grid(row=2, column=1)

        self.priority_label = tk.Label(self.menu_frame, text="Enter task priority (1-5):")
        self.priority_label.grid(row=3, column=0)
        self.priority_entry = tk.Entry(self.menu_frame)
        self.priority_entry.grid(row=3, column=1)

        self.category_label = tk.Label(self.menu_frame, text="Enter task category:")
        self.category_label.grid(row=4, column=0)
        self.category_entry = tk.Entry(self.menu_frame)
        self.category_entry.grid(row=4, column=1)

        # Buttons for actions
        self.add_task_button = tk.Button(self.menu_frame, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=5, column=0, columnspan=2)

        self.display_tasks_button = tk.Button(self.menu_frame, text="Display Tasks", command=self.display_tasks)
        self.display_tasks_button.grid(row=6, column=0, columnspan=2)

        self.display_category_button = tk.Button(self.menu_frame, text="Display Tasks by Category",
                                                 command=self.display_category)
        self.display_category_button.grid(row=7, column=0, columnspan=2)

        self.mark_index_label = tk.Label(self.menu_frame, text="Enter task index to mark as complete:")
        self.mark_index_label.grid(row=10, column=0)
        self.mark_index_entry = tk.Entry(self.menu_frame)
        self.mark_index_entry.grid(row=10, column=1)

        self.mark_complete_button = tk.Button(self.menu_frame, text="Mark Task as Complete", command=self.mark_complete)
        self.mark_complete_button.grid(row=11, column=0, columnspan=2)

    def add_task(self):
        # Add a task based on user input
        description = self.description_entry.get()
        due_date_str = self.due_date_entry.get()
        priority = int(self.priority_entry.get())
        category = self.category_entry.get()

        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            new_task = Task(description, due_date, priority, category)
            self.task_manager.add_task(new_task)
            messagebox.showinfo("Success", "Task added successfully.")
            self.clear_entries()  # Clear the entry boxes after adding a task
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

    def display_tasks(self):
        # Display tasks based on due date
        sorted_tasks = sorted(self.task_manager.priority_queue)

        tasks_text = ""
        for task in sorted_tasks:
            print(task)
            tasks_text += str(task) + "\n"

        self.show_dialog("Tasks", tasks_text)

    def display_category(self):
        # Display tasks based on category
        category = simpledialog.askstring("Display Tasks by Category", "Enter category to filter tasks:")
        if category is not None:
            tasks_text = self.task_manager.display_tasks_to_string(category)
            self.show_dialog(f'Tasks in Category "{category}"', tasks_text)

    def mark_complete(self):
        # Mark a task as complete based on user input
        try:
            task_index = int(self.mark_index_entry.get())
            self.task_manager.mark_task_complete(task_index)
            messagebox.showinfo("Success", "Task marked as complete.")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Invalid task index. Please enter a valid integer.")

    def show_dialog(self, title, message):
        # Display a dialog with given title and message
        dialog = tk.Toplevel(self.menu_frame)
        dialog.title(title)

        text_widget = tk.Text(dialog, height=10, width=40)
        text_widget.insert(tk.END, message)
        text_widget.pack()

        close_button = tk.Button(dialog, text="Close", command=dialog.destroy)
        close_button.pack()

    def clear_entries(self):
        # Clear the content of all entry boxes
        self.description_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.mark_index_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskAppGUI(root)
    root.mainloop()
