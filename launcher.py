import tkinter as tk
from tkinter import ttk
from tools import fprint

def show_page(notebook, page_index):
    notebook.select(page_index)

def main():

    # FOR TESTING:
    return {
        "mode": "host_join",
        "username": "test_user",
        "ip": None
    }

    root = tk.Tk()
    root.title("Black Friday Launcher")
    root.geometry("300x500")

    main.data = {
            "mode": None,
            "username": None,
            "ip": None
        }

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Page for Option 1
    host_join_page = ttk.Frame(notebook)
    notebook.add(host_join_page, text="Host & Join")

    h_j_title = ttk.Label(host_join_page, text="Black Friday Launcher")
    h_j_title.pack(pady=10)

    h_j_page_title = ttk.Label(host_join_page, text="Host & Join")
    h_j_page_title.pack(pady=10)

    h_j_username_label = ttk.Label(host_join_page, text="Username:")
    h_j_username_label.pack(pady=10)
    h_j_username_entry = ttk.Entry(host_join_page)
    h_j_username_entry.pack(pady=10)

    def send_host_join_data():
        main.data = {
            "mode": "host_join",
            "username": h_j_username_entry.get(),
            "ip": None
        }
        root.destroy()  # Close the window

    h_j_host_join_button = ttk.Button(host_join_page, text="Join", command=send_host_join_data)
    h_j_host_join_button.pack(pady=10)

    # Page for Option 2
    join_page = ttk.Frame(notebook)
    notebook.add(join_page, text="Join")

    j_title = ttk.Label(join_page, text="Black Friday Launcher")
    j_title.pack(pady=10)

    j_page_title = ttk.Label(join_page, text="Join")
    j_page_title.pack(pady=10)

    j_username_label = ttk.Label(join_page, text="Username:")
    j_username_label.pack(pady=10)
    j_username_entry = ttk.Entry(join_page)
    j_username_entry.pack(pady=10)

    j_ip_addr_label = ttk.Label(join_page, text="Ip address:")
    j_ip_addr_label.pack(pady=10)
    j_ip_entry = ttk.Entry(join_page)
    j_ip_entry.pack(pady=10)

    def send_join_data():
        main.data = {
            "mode": "join",
            "username": j_username_entry.get(),
            "ip": j_ip_entry.get()
        }
        root.destroy()  # Close the window

    j_join_button = ttk.Button(join_page, text="Join", command=send_join_data)
    j_join_button.pack(pady=10)

    # Page for Option 3
    host_page = ttk.Frame(notebook)
    notebook.add(host_page, text="Host")

    h_title = ttk.Label(host_page, text="Black Friday Launcher")
    h_title.pack(pady=10)

    h_page_title = ttk.Label(host_page, text="Host")
    h_page_title.pack(pady=10)

    h_page_placeholder = ttk.Label(host_page, text="More settings go here later")
    h_page_placeholder.pack(pady=10)

    def send_host_data():
        main.data = {
            "mode": "host",
            "username": None,
            "ip": None
        }
        root.destroy()  # Close the window

    h_host_button = ttk.Button(host_page, text="Host", command=send_host_data)
    h_host_button.pack(pady=10)


    root.mainloop()

    return main.data

if __name__ == "__main__":
    settings = main()
    fprint(settings)