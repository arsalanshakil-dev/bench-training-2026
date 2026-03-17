# CLI Task Manager

> A simple command-line task manager built in Python that lets you add, list, complete, and delete tasks. Tasks are stored locally in a JSON file so your data persists between runs.

---

## Features

* Add new tasks
* Mark tasks as completed
* Delete tasks
* List all tasks
* Filter tasks by status (`todo` or `done`)
* Persistent storage using a JSON file (`tasks.json`)
* Simple and lightweight CLI interface

---

## Requirements

* Python 3.x

No external dependencies are required — everything uses Python's standard library.

---

## Installation

1. Clone or download this repository
2. Navigate to the project folder

```bash
cd your-project-folder
```

3. Run the script using Python

```bash
python app.py
```

---

## Usage

The application is operated through command-line arguments.

### Add a Task

```bash
python app.py add "Buy groceries"
```

---

### List Tasks

```bash
python app.py list
```

---

### Filter Tasks

List only completed tasks:

```bash
python app.py list --filter done
```

List only pending tasks:

```bash
python app.py list --filter todo
```

---

### Mark Task as Done

```bash
python app.py done 1
```

---

### Delete a Task

```bash
python app.py delete 1
```

---

## Data Storage

All tasks are stored in a file named:

```bash
tasks.json
```

Each task contains:

* `id` – Unique identifier
* `title` – Task description
* `status` – `todo` or `done`
* `created_at` – Timestamp of creation

---

## Error Handling

* If `tasks.json` is missing, it will be created automatically.
* If the file is corrupted, the app will reset and start fresh.
* Invalid commands or missing arguments will display usage instructions.

---

## Project Structure

```text
.
├── app.py        # Main application file
├── tasks.json    # Task storage (auto-generated)
```

---

## Future Improvements

* Edit existing tasks
* Add due dates and priorities
* Better CLI parsing using `argparse`
* Colored output for better readability
* Search functionality

---

## Acknowledgements

Built using Python standard libraries:

* `json`
* `sys`
* `datetime`
* `os`

---

## Explain why you used a class here instead of just functions

<!-- Describe the project: its purpose, core features, and who it's for. -->
To bundle data and functions together
