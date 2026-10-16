
import json


def save_devices():
    with open("devices.json", "w") as file:
        json.dump(devices, file, indent=4)


# Load saved devices
try:
    with open("devices.json", "r") as file:
        devices = json.load(file)
except FileNotFoundError:
    devices = []


# Generate the next available ID
if devices:
    id_counter = max(
        int(device["id"].split("-")[1])
        for device in devices
    ) + 1
else:
    id_counter = 1


choice = ""

while choice != "q":
    choice = input(
        "\nWelcome to TechVault!\n"
        "Enter 'a' to add a device.\n"
        "Enter 'l' to list devices.\n"
        "Enter 'd' to delete a device.\n"
        "Enter 's' to search a device.\n"
        "Enter 'q' to quit.\n"
        "Enter 'delete all' to delete all devices.\n"
        "Your choice: "
    ).lower().strip()

    # Add a device
    if choice == "a":
        device_name = input("Device name: ").strip()
        brand = input("Brand: ").strip()
        model = input("Model: ").strip()

        device = {
            "id": f"TV-{id_counter:03}",
            "name": device_name,
            "brand": brand,
            "model": model
        }

        devices.append(device)
        id_counter += 1
        save_devices()

        print("Device added successfully!")

    # List devices
    elif choice == "l":
        if not devices:
            print("No devices registered yet.")
        else:
            for number, device in enumerate(devices, start=1):
                print(f"{number}. Inventory ID: {device['id']}")
                print(f"   Device: {device['name']}")
                print(f"   Brand: {device['brand']}")
                print(f"   Model: {device['model']}")
                print()

    # Delete a device
    elif choice == "d":
        if not devices:
            print("No devices available to delete.")
        else:
            device_delete_id = input(
                "Enter the Inventory ID to delete: "
            ).strip().upper()

            device_to_delete = None

            for device in devices:
                if device_delete_id == device["id"]:
                    device_to_delete = device
                    break

            if device_to_delete is not None:
                devices.remove(device_to_delete)
                save_devices()
                print("Device deleted successfully!")
            else:
                print("Device not found!")

    # Search for a device
    elif choice == "s":
        if not devices:
            print("No devices available to search.")
        else:
            search_id = input(
                "Enter the Inventory ID to search for: "
            ).strip().upper()

            device_found = False

            for device in devices:
                if search_id == device["id"]:
                    print("\nDevice found!")
                    print(f"Inventory ID: {device['id']}")
                    print(f"Device: {device['name']}")
                    print(f"Brand: {device['brand']}")
                    print(f"Model: {device['model']}")

                    device_found = True
                    break

            if not device_found:
                print("Device not found!")
    elif choice == "delete all":
        final_choice=input("This will delete all devices. Are you sure that you want to delete all?y/n:     ")
        if final_choice == "y":
            if not devices:
                print("There's no device to delete.")
            else:
                devices.clear()
                save_devices()
                print("All devices deleted successfully!")
            

        elif final_choice == "n":
            print("Going Back")
            
        else:
            print("You type wrong. Please only type y for continue n for back.")
            
    # Quit the program
    elif choice == "q":
        print("Shutting down TechVault...")

    # Handle invalid choices
    else:
        print("Invalid choice! Please try again.")
