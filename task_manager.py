import json
import os

# Define the filename for storing tasks
TASKS_FILE = 'tasks.json'

class Task:
    """
    A class to represent a Task.
    """
    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

    def to_dict(self):
        """
        Convert the Task instance to a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(task_dict):
        """
        Create a Task instance from a dictionary.
        """
        return Task(
            id=task_dict['id'],
            title=task_dict['title'],
            completed=task_dict['completed']
        )

def load_tasks():
    """
    Load tasks from the JSON file.
    Returns a list of Task instances.
    """
    if not os.path.exists(TASKS_FILE):
        return []

    with open(TASKS_FILE, 'r') as file:
        try:
            tasks_data = json.load(file)
            return [Task.from_dict(task) for task in tasks_data]
        except json.JSONDecodeError:
            print("Error: Corrupted tasks.json file.")
            return []

def save_tasks(tasks):
    """
    Save the list of Task instances to the JSON file.
    """
    with open(TASKS_FILE, 'w') as file:
        tasks_data = [task.to_dict() for task in tasks]
        json.dump(tasks_data, file, indent=4)

def add_task(tasks):
    """
    Add a new task to the task list.
    """
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return
    task_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(id=task_id, title=title)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added with ID {new_task.id}.")

def view_tasks(tasks):
    """
    Display all tasks with their status.
    """
    if not tasks:
        print("No tasks available.")
        return
    print("\nTasks:")
    print("-" * 40)
    for task in tasks:
        status = "✔️ Completed" if task.completed else "❌ Pending"
        print(f"ID: {task.id} | Title: {task.title} | Status: {status}")
    print("-" * 40)

def delete_task(tasks):
    """
    Delete a task by its ID.
    """
    try:
        task_id = int(input("Enter the ID of the task to delete: "))
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return

    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task with ID {task_id} has been deleted.")
            return

    print(f"No task found with ID {task_id}.")

def mark_task_complete(tasks):
    """
    Mark a task as completed by its ID.
    """
    try:
        task_id = int(input("Enter the ID of the task to mark as complete: "))
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return

    for task in tasks:
        if task.id == task_id:
            if task.completed:
                print("Task is already marked as completed.")
            else:
                task.completed = True
                save_tasks(tasks)
                print(f"Task with ID {task_id} has been marked as completed.")
            return

    print(f"No task found with ID {task_id}.")

def display_menu():
    """
    Display the CLI menu options.
    """
    print("\nTask Manager CLI")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Mark Task as Complete")
    print("5. Exit")

def main():
    """
    The main function to run the CLI application.
    """
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            mark_task_complete(tasks)
        elif choice == '5':
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")

if __name__ == "__main__":
    main()
