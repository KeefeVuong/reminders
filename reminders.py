from tkinter import *
from data_store import data_store
import json
from datetime import date

def save():
    store = data_store.get()
    with open("datastore.json", "w") as FILE:
        json.dump(store, FILE)

data = {}

try:
    data = json.load(open("datastore.json", "r"))
except Exception:
    pass

if data:
    data_store.set(data)

def remind_user_exit(remind_user_pop):
    remind_user_pop.destroy()

def remind_user(reminder, date):
    global remind_user_pop
    remind_user_pop = Toplevel(top)
    remind_user_pop.title("Reminder!")
    remind_user_pop.geometry("415x175+775+400")
    remind_user_pop.attributes("-topmost", True)
    remind_user_pop.update()
    remind_user_pop.attributes("-topmost", False)

    reminder_string = StringVar(None)
    reminder_string.set(f"You have a reminder today!\n {date}")
    remind_user_label = Label(remind_user_pop, textvariable=reminder_string, height=4)
    remind_user_label.config(font=('Helvatical bold', 10))
    remind_user_label.grid(row=0, column=5, padx=35)

    reminder_string = StringVar(None)
    reminder_string.set(f"{reminder}")
    remind_user_label = Label(remind_user_pop, textvariable=reminder_string, height=4)
    remind_user_label.config(font=('Helvatical bold', 10))
    remind_user_label.grid(row=1, column=5, padx=37)

    # remind_user_finished_button = Button(remind_user_pop, text="Finished", command=lambda: remind_user_exit(remind_user_pop))
    # remind_user_finished_button.grid(row=2, column=1, columnspan=3)

    # remind_user_delay_button = Button(remind_user_pop, text="Delay (Adds 1 more day)", command=lambda: delay_reminder())
    # remind_user_delay_button.grid(row=4, column=3, pady=15)


def add_reminder(reminders_list, date_entry, reminder_entry):
    new_date = date_entry.get()
    new_string = reminder_entry.get()
    new_reminder = new_date + " - " + new_string

    data = data_store.get()

    reminder_data = {
        "date": new_date,
        "string": new_string
    }

    data["reminders"].append(reminder_data)

    reminders_list.insert(0, new_reminder)
    date_entry.delete(0, END)
    reminder_entry.delete(0, END)

    save()

def delete_reminder(reminders_list):
    removed_item_index = reminders_list.curselection()
    removed_item = reminders_list.get(removed_item_index[0])

    data = data_store.get()

    removed_item_list = removed_item.split(" - ")
    for item in data["reminders"]:
        if item["date"] == removed_item_list[0] and item["string"] == removed_item_list[1]:
            data["reminders"].remove(item)

    index = reminders_list.get(0, END).index(removed_item)
    reminders_list.delete(index)
    save()

def edit_reminder(reminders_list, edit_date_entry, edit_reminder_entry):
    new_date = edit_date_entry.get()
    new_string = edit_reminder_entry.get()
    new_reminder = new_date + " - " + new_string

    data = data_store.get()

    removed_item_index = reminders_list.curselection()
    removed_item = reminders_list.get(removed_item_index[0])

    removed_item_list = removed_item.split(" - ")
    for item in data["reminders"]:
        if item["date"] == removed_item_list[0] and item["string"] == removed_item_list[1]:
            item["date"] = new_date
            item["string"] = new_string

    index = reminders_list.get(0, END).index(removed_item)
    reminders_list.delete(index)
    reminders_list.insert(index, new_reminder)

    data_store.set(data)
    edit_reminder_pop.destroy()
    save()

def edit_reminder_input(reminders_list_listbox):
    global edit_reminder_pop
    edit_reminder_pop = Toplevel(top)
    edit_reminder_pop.title("Edit Reminder")
    edit_reminder_pop.geometry("500x400+650+300")

    date_string = StringVar(None)
    date_string.set("Enter the new date\n (Leave blank if you don't want to change it)")
    edit_date_label = Label(edit_reminder_pop, textvariable=date_string, height=4)
    edit_date_label.grid(row=0, column=0)

    edit_date_str = StringVar(None)
    edit_date_entry = Entry(edit_reminder_pop, textvariable=edit_date_str, width=56)
    edit_date_entry.grid(row=1, column=0, padx=5)

    reminder_string = StringVar(None)
    reminder_string.set("Enter the new reminder\n (Leave blank if you don't want to change it)")
    edit_reminder_label = Label(edit_reminder_pop, textvariable=reminder_string, height=4)
    edit_reminder_label.grid(row=2, column=0)

    edit_reminder_str = StringVar(None)
    edit_reminder_entry = Entry(edit_reminder_pop, textvariable=edit_reminder_str, width=56)
    edit_reminder_entry.grid(row=3, column=0, padx=5)

    submit_button = Button(edit_reminder_pop, text="Submit", command=lambda: edit_reminder(reminders_list_listbox, edit_date_entry, edit_reminder_entry))
    submit_button.grid(row=4, column=0, pady=25)

top = Tk()
top.title("Reminder Application")
top.geometry("500x400+650+300")

top.grid_columnconfigure(0, weight=0)
top.grid_columnconfigure(1, weight=5)

date_label_str = StringVar()
date_label_str.set("Enter the date \n(DD/MM/YYYY)")

date_label = Label(top, textvariable=date_label_str, height=4)
date_label.grid(row=0, column=0)

date_entry_str = StringVar(None)
date_entry = Entry(top, textvariable=date_entry_str, width=100)
date_entry.grid(row=0, column=1, padx=25, columnspan=3)

reminder_label_str = StringVar()
reminder_label_str.set("Enter the reminder")

reminder_label = Label(top, textvariable=reminder_label_str, height=4)
reminder_label.grid(row=1, column=0, padx=5)

reminder_entry_str = StringVar(None)
reminder_entry = Entry(top, textvariable=reminder_entry_str, width=100)
reminder_entry.grid(row=1, column=1, padx=25, columnspan=3)

add_reminder_button = Button(top, text="Add Reminder", command=lambda: add_reminder(reminders_list_listbox, date_entry, reminder_entry))
add_reminder_button.grid(row=2, column=1)

reminders_list_label_str = StringVar()
reminders_list_label_str.set("Current reminders")

reminders_list_label = Label(top, textvariable=reminders_list_label_str, height=4)
reminders_list_label.grid(row=3, column=0)

reminders_list_scrollbar = Scrollbar(top, orient=VERTICAL)
reminders_list_scrollbar.grid(row=4, column=5, sticky='ns')

reminders_list_listbox = Listbox(top, yscrollcommand=reminders_list_scrollbar.set, width=75, height=30)

if data:
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    for item in data["reminders"]:
        if item["date"] <= today:
            remind_user(item["string"], item["date"])
        reminder_string = item["date"] + " - " + item["string"]
        reminders_list_listbox.insert(END, reminder_string)

reminders_list_listbox.grid(row=4, column=0, columnspan=5)

reminders_list_scrollbar.config(command=reminders_list_listbox.yview)

edit_reminder_button = Button(top, text="Edit Reminder", command=lambda: edit_reminder_input(reminders_list_listbox))
edit_reminder_button.grid(row=3, column=1)

delete_reminder_button = Button(top, text="Delete Reminder", command=lambda: delete_reminder(reminders_list_listbox))
delete_reminder_button.grid(row=3, column=2)

top.mainloop()