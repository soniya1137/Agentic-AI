#!/usr/bin/env python3
"""Simple to-do list CLI. Tasks are stored in todo.json next to this script."""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DB = Path(__file__).with_name("todo.json")


def load():
    if DB.exists():
        return json.loads(DB.read_text(encoding="utf-8"))
    return []


def save(tasks):
    DB.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def cmd_add(args):
    tasks = load()
    next_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({
        "id": next_id,
        "text": " ".join(args.text),
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds"),
    })
    save(tasks)
    print(f"Added task {next_id}.")


def cmd_list(args):
    tasks = load()
    if not args.all:
        tasks = [t for t in tasks if not t["done"]]
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        mark = "x" if t["done"] else " "
        print(f"[{mark}] {t['id']:>3}  {t['text']}")


def find(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    sys.exit(f"No task with id {task_id}.")


def cmd_done(args):
    tasks = load()
    find(tasks, args.id)["done"] = True
    save(tasks)
    print(f"Task {args.id} marked as done.")


def cmd_delete(args):
    tasks = load()
    find(tasks, args.id)
    save([t for t in tasks if t["id"] != args.id])
    print(f"Task {args.id} deleted.")


def build_parser():
    parser = argparse.ArgumentParser(description="Simple to-do list CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="add a task")
    p.add_argument("text", nargs="+", help="task description")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="show tasks")
    p.add_argument("-a", "--all", action="store_true", help="include done tasks")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("done", help="mark a task as done")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("delete", help="delete a task")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_delete)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
