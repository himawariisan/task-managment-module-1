from task_manager.manager import TaskManager
 
 
def print_menu():
    print("\n=== Task Management System ===")
    print("1. Add task")
    print("2. Delete task")
    print("3. List tasks")
    print("4. Mark task as completed (and remove)")
    print("5. Exit")

def main():
    manager = TaskManager()
 
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
 
        if choice == "1":
            desc = input("Description: ").strip()
            try:
                priority = int(input("Priority (1-5, where 1 is highest): ").strip())
                task = manager.add_task(desc, priority)
                print(f"\nTask added:\n{task}")
            except ValueError as e:
                print(f"Error: {e}")
 
        elif choice == "2":
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                manager.delete_task(task_id)
                print(f"Task {task_id} deleted.")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")
 
        elif choice == "3":
            sort_by = input("Sort by (priority/creation_date) [default: priority]: ").strip()
            if sort_by not in ("priority", "creation_date"):
                sort_by = "priority"
            tasks = manager.list_tasks(sort_by=sort_by)
            if not tasks:
                print("No tasks found.")
            else:
                print(f"\n--- Tasks sorted by {sort_by} ---")
                for task in tasks:
                    print(task)
                    print("-" * 30)
 
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to complete and remove: ").strip())
                task = manager.complete_and_remove_task(task_id)
                print(f"Task {task_id} marked as completed and removed.")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")
 
        elif choice == "5":
            print("Goodbye!")
            break
 
        else:
            print("Invalid option. Please try again.")
 

if __name__ == "__main__":
    main()
