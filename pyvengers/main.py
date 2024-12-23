import json
import os

# File to store PyVenger profiles
DATA_FILE = os.path.join(os.path.dirname(__file__), "pyvengers.json")

def add_pyvenger(name, superpower, mission):
    """Add a new PyVenger to the list."""
    new_pyvenger = {"name": name, "superpower": superpower, "mission": mission}
    pyvengers = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            pyvengers = json.load(file)

    pyvengers.append(new_pyvenger)

    with open(DATA_FILE, "w") as file:
        json.dump(pyvengers, file, indent=4)

    print(f"🎉 {name} has been added to the PyVengers!")

def list_pyvengers():
    """List all PyVengers."""
    if not os.path.exists(DATA_FILE):
        print("No PyVengers yet! Add one now.")
        return

    with open(DATA_FILE, "r") as file:
        pyvengers = json.load(file)

    if not pyvengers:
        print("No PyVengers yet! Add one now.")
        return

    print("\n📜 PyVengers List:")
    for member in pyvengers:
        print(f"- {member['name']} ({member['superpower']}): {member['mission']}")

def interactive_menu():
    """Interactive CLI menu."""
    while True:
        print("\nWelcome to PyVengers Assemble!")
        print("1. Add a PyVenger")
        print("2. List all PyVengers")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            superpower = input("Enter superpower: ")
            mission = input("Enter mission: ")
            add_pyvenger(name, superpower, mission)
        elif choice == "2":
            list_pyvengers()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    interactive_menu()
