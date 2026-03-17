import json
import sys
from datetime import datetime
import os

FILE_NAME = "tasks.json"

class Task:
    def __init__(self, id, title, status="todo", created_at=None):
        self.id = id
        self.title = title
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()

    def mark_completed(self):
        self.status = "done"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["id"],
            data["title"],
            data["status"],
            data["created_at"],
        )


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title):
        new_id = 1 if not self.tasks else max(t.id for t in self.tasks) + 1
        task = Task(new_id, title)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added with ID {new_id}")

    def complete_task(self, id):
        task = self._find_task(id)
        if task:
            task.mark_completed()
            self.save_tasks()
            print(f"Task {id} marked as done")
        else:
            print(f"Error: Task with ID {id} not found")

    def delete_task(self, id):
        task = self._find_task(id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Task {id} deleted")
        else:
            print(f"Error: Task with ID {id} not found")

    def list_tasks(self, filter=None):
        filtered = self.tasks

        if filter == "done":
            filtered = [t for t in self.tasks if t.status == "done"]
        elif filter == "todo":
            filtered = [t for t in self.tasks if t.status == "todo"]

        if not filtered:
            print("No tasks found.")
            return

        for t in filtered:
            print(f"[{t.id}] {t.title} ({t.status}) - {t.created_at}")

    def _find_task(self, id):
        return next((t for t in self.tasks if t.id == id), None)

    def save_tasks(self):
        try:
            with open(FILE_NAME, "w") as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        if not os.path.exists(FILE_NAME):
            self.tasks = []
            return

        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data]
        except json.JSONDecodeError:
            print("Warning: tasks.json is corrupted. Starting fresh.")
            self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []


# -------- CLI -------- #

def main():
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Usage: add | done | list | delete")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: add 'task title'")
            return
        title = sys.argv[2]
        manager.add_task(title)

    elif command == "done":
        if len(sys.argv) < 3:
            print("Usage: done <id>")
            return
        manager.complete_task(int(sys.argv[2]))

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: delete <id>")
            return
        manager.delete_task(int(sys.argv[2]))

    elif command == "list":
        if len(sys.argv) > 3 and sys.argv[2] == "--filter":
            manager.list_tasks(sys.argv[3])
        else:
            manager.list_tasks()

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()