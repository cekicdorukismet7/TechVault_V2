import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from datetime import datetime


# ==========================================================
# CONFIGURATION
# ==========================================================

APP_NAME = "TechVault"
APP_VERSION = "2.0.0"

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "devices.json"
META_FILE = APP_DIR / "techvault_meta.json"
BACKUP_FILE = APP_DIR / "devices_backup.json"

BG = "#0B1120"
SIDEBAR = "#111827"
PANEL = "#172033"
PANEL_LIGHT = "#202C42"
ACCENT = "#38BDF8"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#34D399"
RED = "#FB7185"
BORDER = "#29364B"

FONT = "Segoe UI"

devices = []
next_id = 1


# ==========================================================
# DATA MANAGEMENT
# ==========================================================

def atomic_write_json(path, data):
    """Save JSON using a temporary file."""
    temp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, path)

    finally:
        if temp_path.exists():
            temp_path.unlink()


def load_data():
    """Load existing device data without resetting invalid files."""
    global devices, next_id

    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                loaded = json.load(file)

            if not isinstance(loaded, list):
                raise ValueError("Device data must be a JSON list.")

            for device in loaded:
                if not isinstance(device, dict):
                    raise ValueError("Invalid device record.")

                for key in ("id", "name", "brand", "model"):
                    if key not in device:
                        raise ValueError(f"Missing field: {key}")

            devices = loaded

        except (OSError, ValueError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Data Error",
                f"Could not load devices.json:\n\n{error}\n\n"
                "Your original file has not been overwritten."
            )
            raise SystemExit(1)

    if META_FILE.exists():
        try:
            with open(META_FILE, "r", encoding="utf-8") as file:
                metadata = json.load(file)

            saved_id = metadata.get("next_id", 1)

            if not isinstance(saved_id, int) or saved_id < 1:
                raise ValueError("Invalid next_id value.")

            next_id = saved_id

        except (OSError, ValueError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Metadata Error",
                f"Could not load metadata:\n{error}"
            )
            raise SystemExit(1)

    used_ids = []

    for device in devices:
        device_id = str(device["id"])

        if device_id.startswith("TV-"):
            try:
                used_ids.append(int(device_id[3:]))
            except ValueError:
                pass

    if used_ids:
        next_id = max(next_id, max(used_ids) + 1)


def save_data():
    """Save device records and ID metadata."""
    global next_id

    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                old_data = json.load(file)

            if not isinstance(old_data, list):
                raise ValueError("Existing device data is invalid.")

            atomic_write_json(BACKUP_FILE, old_data)

        atomic_write_json(DATA_FILE, devices)
        atomic_write_json(META_FILE, {"next_id": next_id})

        return True

    except (OSError, ValueError, json.JSONDecodeError) as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save your changes:\n\n{error}"
        )
        return False


def generate_id():
    """Generate a unique sequential device ID."""
    global next_id

    device_id = f"TV-{next_id:03d}"
    next_id += 1

    return device_id


def find_device(device_id):
    """Find a device using its ID."""
    for device in devices:
        if str(device["id"]) == str(device_id):
            return device

    return None


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()
root.title(f"{APP_NAME} | Smart Inventory System")
root.geometry("1180x760")
root.minsize(900, 600)
root.configure(bg=BG)

# Three rows: header/content, footer.
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Treeview",
    background=PANEL,
    foreground=TEXT,
    fieldbackground=PANEL,
    rowheight=36,
    borderwidth=0,
    font=(FONT, 10)
)

style.configure(
    "Treeview.Heading",
    background=SIDEBAR,
    foreground=MUTED,
    font=(FONT, 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#075985")],
    foreground=[("selected", "white")]
)

style.configure(
    "Vertical.TScrollbar",
    background=PANEL_LIGHT,
    troughcolor=BG,
    arrowcolor=TEXT,
    bordercolor=BG
)


# ==========================================================
# MAIN LAYOUT
# ==========================================================

main_container = tk.Frame(root, bg=BG)
main_container.grid(row=0, column=0, sticky="nsew")

main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(1, weight=1)

sidebar = tk.Frame(main_container, bg=SIDEBAR, width=220)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

content = tk.Frame(main_container, bg=BG)
content.grid(row=0, column=1, sticky="nsew")

content.grid_rowconfigure(3, weight=1)
content.grid_columnconfigure(0, weight=1)


# ==========================================================
# REUSABLE UI FUNCTIONS
# ==========================================================

def make_button(parent, text, command, color=ACCENT, fg=BG):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground="#0EA5E9",
        activeforeground="white",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        font=(FONT, 10, "bold"),
        padx=14,
        pady=9
    )


def make_stat_card(parent, title):
    card = tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        bg=PANEL,
        fg=MUTED,
        font=(FONT, 10)
    ).pack(anchor="w", padx=15, pady=(12, 3))

    value = tk.Label(
        card,
        text="0",
        bg=PANEL,
        fg=TEXT,
        font=(FONT, 24, "bold")
    )
    value.pack(anchor="w", padx=15, pady=(0, 12))

    return card, value


# ==========================================================
# SIDEBAR
# ==========================================================

tk.Label(
    sidebar,
    text="TECHVAULT",
    bg=SIDEBAR,
    fg=ACCENT,
    font=(FONT, 21, "bold")
).pack(anchor="w", padx=20, pady=(28, 2))

tk.Label(
    sidebar,
    text="SMART INVENTORY SYSTEM",
    bg=SIDEBAR,
    fg=MUTED,
    font=(FONT, 8, "bold")
).pack(anchor="w", padx=21, pady=(0, 30))


def sidebar_button(text, command):
    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=SIDEBAR,
        fg=TEXT,
        activebackground=PANEL_LIGHT,
        activeforeground=ACCENT,
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        anchor="w",
        font=(FONT, 10),
        padx=20,
        pady=13
    )
    button.pack(fill="x", padx=7, pady=2)

    return button


# ==========================================================
# HEADER
# ==========================================================

header = tk.Frame(content, bg=BG)
header.grid(row=0, column=0, sticky="ew", padx=26, pady=(24, 18))

header.grid_columnconfigure(0, weight=1)

tk.Label(
    header,
    text="Inventory Dashboard",
    bg=BG,
    fg=TEXT,
    font=(FONT, 23, "bold")
).grid(row=0, column=0, sticky="w")

tk.Label(
    header,
    text="Manage and organize your technical equipment.",
    bg=BG,
    fg=MUTED,
    font=(FONT, 10)
).grid(row=1, column=0, sticky="w", pady=(5, 0))

make_button(
    header,
    "+ Add Device",
    lambda: open_device_form()
).grid(row=0, column=1, rowspan=2, padx=(12, 0))


# ==========================================================
# STATISTICS
# ==========================================================

stats = tk.Frame(content, bg=BG)
stats.grid(row=1, column=0, sticky="ew", padx=26, pady=(0, 20))

total_card, total_value = make_stat_card(stats, "Total Devices")
brands_card, brands_value = make_stat_card(stats, "Unique Brands")
visible_card, visible_value = make_stat_card(stats, "Visible Results")

for index, card in enumerate(
    (total_card, brands_card, visible_card)
):
    card.grid(
        row=0,
        column=index,
        sticky="ew",
        padx=(0 if index == 0 else 8, 0)
    )
    stats.grid_columnconfigure(index, weight=1)


# ==========================================================
# INVENTORY AREA
# ==========================================================

inventory = tk.Frame(content, bg=BG)
inventory.grid(row=2, column=0, sticky="ew", padx=26, pady=(0, 10))

tk.Label(
    inventory,
    text="Device Inventory",
    bg=BG,
    fg=TEXT,
    font=(FONT, 15, "bold")
).pack(side="left")

tk.Label(
    inventory,
    text=f"Version {APP_VERSION}",
    bg=BG,
    fg=MUTED,
    font=(FONT, 9)
).pack(side="right")


# ==========================================================
# SEARCH AND FILTERS
# ==========================================================

controls = tk.Frame(content, bg=BG)
controls.grid(row=3, column=0, sticky="nsew", padx=26, pady=(0, 12))

controls.grid_rowconfigure(1, weight=1)
controls.grid_columnconfigure(0, weight=1)

search_var = tk.StringVar()
filter_var = tk.StringVar(value="All")
sort_var = tk.StringVar(value="ID")

control_bar = tk.Frame(controls, bg=BG)
control_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))

search_entry = tk.Entry(
    control_bar,
    textvariable=search_var,
    bg=PANEL,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    font=(FONT, 10),
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=ACCENT
)
search_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

filter_box = ttk.Combobox(
    control_bar,
    textvariable=filter_var,
    values=["All", "With Brand", "Without Brand"],
    state="readonly",
    width=14
)
filter_box.pack(side="left", padx=5, ipady=4)

sort_box = ttk.Combobox(
    control_bar,
    textvariable=sort_var,
    values=["ID", "Name", "Brand", "Model"],
    state="readonly",
    width=9
)
sort_box.pack(side="left", padx=5, ipady=4)

make_button(
    control_bar,
    "Clear",
    lambda: search_var.set(""),
    color=PANEL_LIGHT,
    fg=TEXT
).pack(side="left", padx=(5, 0))


# ==========================================================
# DEVICE TABLE
# ==========================================================

table_frame = tk.Frame(
    controls,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_frame.grid(row=1, column=0, sticky="nsew")

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

columns = ("id", "name", "brand", "model")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

tree.heading("id", text="DEVICE ID")
tree.heading("name", text="DEVICE NAME")
tree.heading("brand", text="BRAND")
tree.heading("model", text="MODEL")

tree.column("id", width=110, minwidth=90)
tree.column("name", width=230, minwidth=130)
tree.column("brand", width=160, minwidth=100)
tree.column("model", width=160, minwidth=100)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=8)


# ==========================================================
# ACTION BAR
# ==========================================================

actions = tk.Frame(content, bg=BG)
actions.grid(row=4, column=0, sticky="ew", padx=26, pady=(0, 14))

make_button(
    actions,
    "Edit Selected",
    lambda: edit_selected(),
    color=PANEL_LIGHT,
    fg=TEXT
).pack(side="left", padx=(0, 8))

make_button(
    actions,
    "Delete Selected",
    lambda: delete_selected(),
    color="#7F1D1D",
    fg="white"
).pack(side="left", padx=(0, 8))

make_button(
    actions,
    "Delete All",
    lambda: delete_all(),
    color="#991B1B",
    fg="white"
).pack(side="left")

make_button(
    actions,
    "Refresh",
    lambda: refresh_table(),
    color=PANEL_LIGHT,
    fg=TEXT
).pack(side="right")


# ==========================================================
# FIXED FOOTER — MADE WITH AI
# ==========================================================

footer = tk.Frame(
    root,
    bg="#111827",
    height=40,
    highlightbackground=BORDER,
    highlightthickness=1
)

footer.grid(row=1, column=0, sticky="ew")
footer.grid_propagate(False)

footer.grid_columnconfigure(0, weight=1)
footer.grid_columnconfigure(1, weight=0)

# The AI credit is permanently placed on the left.
tk.Label(
    footer,
    text="Made with AI  •  Built with Python",
    bg="#111827",
    fg=ACCENT,
    font=(FONT, 10, "bold")
).grid(row=0, column=0, sticky="w", padx=16, pady=9)

status_label = tk.Label(
    footer,
    text="Ready",
    bg="#111827",
    fg=GREEN,
    font=(FONT, 9)
)

status_label.grid(row=0, column=1, sticky="e", padx=16, pady=9)


# ==========================================================
# VALIDATION
# ==========================================================

def validate_fields(name, brand, model):
    name = name.strip()
    brand = brand.strip()
    model = model.strip()

    if not name:
        messagebox.showwarning(
            "Validation Error",
            "Device name is required."
        )
        return None

    if any(len(value) > 100 for value in (name, brand, model)):
        messagebox.showwarning(
            "Validation Error",
            "Each field must be 100 characters or fewer."
        )
        return None

    return {
        "name": name,
        "brand": brand,
        "model": model
    }


# ==========================================================
# ADD AND EDIT DEVICE
# ==========================================================

def open_device_form(device=None):
    editing = device is not None

    form = tk.Toplevel(root)
    form.title("Edit Device" if editing else "Add Device")
    form.geometry("420x420")
    form.resizable(False, False)
    form.configure(bg=BG)
    form.transient(root)
    form.grab_set()

    tk.Label(
        form,
        text="Edit Device" if editing else "Add New Device",
        bg=BG,
        fg=TEXT,
        font=(FONT, 19, "bold")
    ).pack(anchor="w", padx=25, pady=(25, 5))

    tk.Label(
        form,
        text="Enter the device information.",
        bg=BG,
        fg=MUTED,
        font=(FONT, 10)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    fields = {}

    for field in ("Name", "Brand", "Model"):
        tk.Label(
            form,
            text=field,
            bg=BG,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor="w", padx=25, pady=(8, 4))

        entry = tk.Entry(
            form,
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=(FONT, 10)
        )
        entry.pack(fill="x", padx=25, ipady=8)

        if editing:
            entry.insert(0, device.get(field.lower(), ""))

        fields[field] = entry

    def submit():
        values = validate_fields(
            fields["Name"].get(),
            fields["Brand"].get(),
            fields["Model"].get()
        )

        if values is None:
            return

        if editing:
            previous = device.copy()
            device.update(values)

            if not save_data():
                device.clear()
                device.update(previous)
                return

            status_label.config(text="Device updated")

        else:
            new_device = {
                "id": generate_id(),
                **values,
                "created_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

            devices.append(new_device)

            if not save_data():
                devices.remove(new_device)
                return

            status_label.config(text="Device added")

        refresh_table()
        form.destroy()

        messagebox.showinfo(
            "Success",
            "Device saved successfully."
        )

    make_button(
        form,
        "Save Device",
        submit
    ).pack(fill="x", padx=25, pady=22)


# ==========================================================
# SEARCH, FILTER AND SORT
# ==========================================================

def get_visible_devices():
    query = search_var.get().strip().casefold()
    selected_filter = filter_var.get()
    selected_sort = sort_var.get()

    result = []

    for device in devices:
        text = " ".join(
            str(device.get(field, ""))
            for field in ("id", "name", "brand", "model")
        ).casefold()

        if query and query not in text:
            continue

        brand = str(device.get("brand", "")).strip()

        if selected_filter == "With Brand" and not brand:
            continue

        if selected_filter == "Without Brand" and brand:
            continue

        result.append(device)

    sort_keys = {
        "ID": lambda item: str(item.get("id", "")),
        "Name": lambda item: str(item.get("name", "")).casefold(),
        "Brand": lambda item: str(item.get("brand", "")).casefold(),
        "Model": lambda item: str(item.get("model", "")).casefold()
    }

    result.sort(key=sort_keys.get(selected_sort, sort_keys["ID"]))

    return result


def refresh_table(*_):
    for item in tree.get_children():
        tree.delete(item)

    visible_devices = get_visible_devices()

    for device in visible_devices:
        tree.insert(
            "",
            "end",
            values=(
                device.get("id", ""),
                device.get("name", ""),
                device.get("brand", ""),
                device.get("model", "")
            )
        )

    total_value.config(text=str(len(devices)))

    unique_brands = {
        str(device.get("brand", "")).strip().casefold()
        for device in devices
        if str(device.get("brand", "")).strip()
    }

    brands_value.config(text=str(len(unique_brands)))
    visible_value.config(text=str(len(visible_devices)))

    status_label.config(
        text=f"Showing {len(visible_devices)} of {len(devices)} devices"
    )


# ==========================================================
# SELECTION, EDITING AND DELETION
# ==========================================================

def get_selected_device():
    selection = tree.selection()

    if not selection:
        messagebox.showwarning(
            "No Selection",
            "Select a device from the table first."
        )
        return None

    values = tree.item(selection[0], "values")

    if not values:
        return None

    device = find_device(values[0])

    if device is None:
        refresh_table()
        messagebox.showerror(
            "Not Found",
            "The selected device no longer exists."
        )

    return device


def edit_selected():
    device = get_selected_device()

    if device is not None:
        open_device_form(device)


def delete_selected():
    device = get_selected_device()

    if device is None:
        return

    confirmed = messagebox.askyesno(
        "Confirm Deletion",
        f"Delete {device['id']} — {device['name']}?"
    )

    if not confirmed:
        return

    index = devices.index(device)
    devices.pop(index)

    if not save_data():
        devices.insert(index, device)
        return

    refresh_table()

    messagebox.showinfo(
        "Deleted",
        f"{device['id']} was deleted."
    )


def delete_all():
    if not devices:
        messagebox.showinfo(
            "Inventory Empty",
            "There are no devices to delete."
        )
        return

    confirmed = messagebox.askyesno(
        "Delete All",
        f"Delete all {len(devices)} devices?\n\n"
        "A backup of the previous saved list is attempted."
    )

    if not confirmed:
        return

    previous_devices = devices.copy()
    devices.clear()

    if not save_data():
        devices.extend(previous_devices)
        return

    refresh_table()

    messagebox.showinfo(
        "Inventory Cleared",
        "All devices were deleted."
    )


# ==========================================================
# NAVIGATION
# ==========================================================

def show_dashboard():
    search_var.set("")
    filter_var.set("All")
    sort_var.set("ID")
    refresh_table()


sidebar_button("▦   Dashboard", show_dashboard)
sidebar_button("＋   Add Device", lambda: open_device_form())
sidebar_button("✎   Edit Selected", edit_selected)
sidebar_button("⌕   Search Inventory", lambda: search_entry.focus_set())
sidebar_button("↻   Refresh Data", refresh_table)
sidebar_button("×   Delete Selected", delete_selected)
sidebar_button("⚠   Delete All", delete_all)


# ==========================================================
# KEYBOARD SHORTCUTS
# ==========================================================

root.bind("<Delete>", lambda _event: delete_selected())
root.bind("<Control-n>", lambda _event: open_device_form())
root.bind("<Control-f>", lambda _event: search_entry.focus_set())

search_var.trace_add("write", refresh_table)
filter_var.trace_add("write", refresh_table)
sort_var.trace_add("write", refresh_table)


# ==========================================================
# START APPLICATION
# ==========================================================

load_data()
refresh_table()

root.mainloop()
