import json
from pathlib import Path

DATA_FILE = Path("contacts.json")
contacts = {}

# ---------- Persistence ----------

def load_contacts():
    global contacts
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            contacts = json.load(f)
    else:
        contacts = {}

def save_contacts():
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# ---------- Helpers ----------

def normalize(name: str) -> str:
    return name.strip().lower()

def confirm(msg: str) -> bool:
    return input(f"{msg} (y/n): ").strip().lower() == "y"

# ---------- CRUD Operations ----------

def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter number: ").strip()

    if not name or not phone:
        print("Name and number cannot be empty")
        return

    key = normalize(name)

    if key in contacts:
        print("Contact already exists")
        return

    contacts[key] = {
        "name": name,
        "phone": phone
    }

    save_contacts()
    print("Contact added")

def delete_contact():
    name = input("Enter name to delete: ").strip()
    key = normalize(name)

    if key not in contacts:
        print("Contact does not exist")
        return

    if not confirm(f"Delete {contacts[key]['name']}?"):
        print("Delete cancelled")
        return

    del contacts[key]
    save_contacts()
    print("Contact deleted")

def edit_contact():
    name = input("Enter name to edit: ").strip()
    key = normalize(name)

    if key not in contacts:
        print("Contact does not exist")
        return

    contact = contacts[key]
    print(f"Current number: {contact['phone']}")

    print("1. Edit name")
    print("2. Edit number")
    choice = input("Choose: ").strip()

    if choice == "1":
        new_name = input("Enter new name: ").strip()
        new_key = normalize(new_name)

        if not new_name:
            print("Name cannot be empty")
            return

        if new_key in contacts:
            print("Another contact already has this name")
            return

        contacts[new_key] = {
            "name": new_name,
            "phone": contact["phone"]
        }
        del contacts[key]

    elif choice == "2":
        new_phone = input("Enter new number: ").strip()
        if not new_phone:
            print("Number cannot be empty")
            return
        contact["phone"] = new_phone

    else:
        print("Invalid choice")
        return

    save_contacts()
    print("Contact updated")

def search_contact():
    name = input("Enter name to search: ").strip()
    key = normalize(name)

    if key in contacts:
        c = contacts[key]
        print(f"{c['name']} → {c['phone']}")
    else:
        print("Contact not found")

def show_all():
    if not contacts:
        print("No contacts found")
        return

    print("\n--- All Contacts ---")
    for c in contacts.values():
        print(f"{c['name']} → {c['phone']}")

# ---------- Menu ----------

def menu():
    while True:
        print("\n--- Contact Book ---")
        print("1. Add")
        print("2. Delete")
        print("3. Edit")
        print("4. Search")
        print("5. Show All")
        print("6. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            delete_contact()
        elif choice == "3":
            edit_contact()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            show_all()
        elif choice == "6":
            print("Goodbye")
            break
        else:
            print("Invalid option")

# ---------- Entry Point ----------

if __name__ == "__main__":
    load_contacts()
    menu()
