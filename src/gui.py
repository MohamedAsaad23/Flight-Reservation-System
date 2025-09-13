from tkinter import *
from database import Database
from core import find_shortest_path

class ShortestPathApp:

    def __init__(self):
        self.root = Tk()
        self.root.title("Flight Reservation System")
        self.root.resizable(False, False)
        self.root.geometry("1300x700")

        # Create a database instance
        self.db = Database()

        # Create header
        header_label = Label(self.root, text="Flight Reservation System",
                             bg="#2C3E50", fg="white",
                             font=("Helvetica", 35, "bold"), pady=10)
        header_label.pack(fill=X)

        # Buttons section
        self.button_frame = Frame(self.root, bd=5, relief=RIDGE, bg="#3498DB")
        self.button_frame.place(x=20, y=90, width=1260, height=70)

        buttons_row = Frame(self.button_frame, bg="#3498DB")
        buttons_row.pack(side=TOP, pady=15)

        # ---- Buttons ----
        Button(buttons_row, text="Find Shortest Path", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_find_path).grid(row=0, column=1, padx=10)

        Button(buttons_row, text="Add Airport", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_add_airport).grid(row=0, column=2, padx=10)

        Button(buttons_row, text="Delete Airport", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_delete_airport).grid(row=0, column=3, padx=10)

        Button(buttons_row, text="Add Flight", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_add_flight).grid(row=0, column=4, padx=10)

        Button(buttons_row, text="Delete Flight", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_delete_flight).grid(row=0, column=5, padx=10)

        Button(buttons_row, text="Get All Airports", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_all_airports).grid(row=0, column=6, padx=10)

        Button(buttons_row, text="Get All Flights", width=20,
               bg="#2C3E50", fg="white", activebackground="#34495E",
               command=self.show_all_flights).grid(row=0, column=7, padx=10)

        # Content section
        self.content_frame = Frame(self.root, bd=5, relief=RIDGE, bg="#ECF0F1")
        self.content_frame.place(x=20, y=180, width=1260, height=510)
        
        # Show default page
        self.show_find_path()

    # ---- Clear Content from Content section ----
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ---- Styled title bar ----
    def styled_title(self, text):
        title_frame = Frame(self.content_frame, bg="#2C3E50", bd=3, relief="ridge")
        title_frame.pack(pady=(10, 20))
        Label(title_frame, text=text,
              bg="#2C3E50", fg="white",
              font=("Helvetica", 22, "bold"), padx=20, pady=10).pack()

    # ---- Find Path ----
    def show_find_path(self):
        self.clear_content()
        self.styled_title("Find Shortest Path")

        form_frame = Frame(self.content_frame, bg="white", bd=2, relief="groove")
        form_frame.pack(pady=20)

        Label(form_frame, text="Start Airport:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        start_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        start_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="End Airport:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        end_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        end_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(form_frame, text="Find Path",
               command=lambda: self.find_path(start_entry.get(), end_entry.get()),
               bg="#3498DB", fg="white", activebackground="#2980B9",
               relief="raised", bd=2).grid(row=2, columnspan=2, pady=20)

    def find_path(self, start, end):
        cost, path = find_shortest_path(self.db, start, end)
        if cost == float("inf"):
            Label(self.content_frame, text="No path found!", fg="red").pack()
        else:
            Label(self.content_frame,
                  text=f"Path: {' -> '.join(path)} | Total Cost: ${cost:.2f}",
                  fg="green").pack()

    # ---- Add Airport ----
    def show_add_airport(self):
        self.clear_content()
        self.styled_title("Add Airport")

        form_frame = Frame(self.content_frame, bg="white", bd=2, relief="groove")
        form_frame.pack(pady=20)

        Label(form_frame, text="Airport Name:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(form_frame, text="Add Airport",
               command=lambda: self.add_airport(name_entry.get()),
               bg="#27AE60", fg="white",
               activebackground="#229954", activeforeground="white",
               relief="raised", bd=2).grid(row=1, columnspan=2, pady=20)

    def add_airport(self, name):
        if name:
            result = self.db.add_airport(name)
            if result == "success":
                Label(self.content_frame, text=f"Airport '{name}' added!", fg="green").pack()
            elif result == "exists":
                Label(self.content_frame, text=f"Airport '{name}' already exists!", fg="red").pack()

    # ---- Delete Airport ----
    def show_delete_airport(self):
        self.clear_content()
        self.styled_title("Delete Airport")

        form_frame = Frame(self.content_frame, bg="white", bd=2, relief="groove")
        form_frame.pack(pady=20)

        Label(form_frame, text="Airport Name:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(form_frame, text="Delete Airport",
               command=lambda: self.delete_airport(name_entry.get()),
               bg="#C0392B", fg="white",
               activebackground="#922B21", activeforeground="white",
               relief="raised", bd=2).grid(row=1, columnspan=2, pady=20)

    def delete_airport(self, name):
        if name:
            result = self.db.delete_airport(name)
            if result == "success":
                Label(self.content_frame, text=f"Airport '{name}' deleted!", fg="red").pack()
            elif result == "not_found":
                Label(self.content_frame, text=f"Airport '{name}' does not exist!", fg="red").pack()

    # ---- Add Flight ----
    def show_add_flight(self):
        self.clear_content()
        self.styled_title("Add Flight")

        form_frame = Frame(self.content_frame, bg="white", bd=2, relief="groove")
        form_frame.pack(pady=20)

        Label(form_frame, text="Source Airport:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        src_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        src_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Destination Airport:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        dest_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        dest_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Cost:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        cost_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        cost_entry.grid(row=2, column=1, padx=5, pady=5)

        Button(form_frame, text="Add Flight",
               command=lambda: self.add_flight(src_entry.get(), dest_entry.get(), cost_entry.get()),
               bg="#27AE60", fg="white",
               activebackground="#229954", activeforeground="white",
               relief="raised", bd=2).grid(row=3, columnspan=2, pady=20)

    def add_flight(self, src, dest, cost):
        try:
            cost = float(cost)
            result = self.db.add_flight(src, dest, cost)
            if result == "no_airport":
                Label(self.content_frame, text=f"One or both airports '{src}', '{dest}' do not exist!", fg="red").pack()
            elif result == "exists":
                Label(self.content_frame, text=f"Flight {src} -> {dest} already exists!", fg="red").pack()
            elif result == "success":
                Label(self.content_frame, text=f"Flight {src} -> {dest} added!", fg="green").pack()
        except ValueError:
            Label(self.content_frame, text="Cost must be a number!", fg="red").pack()

    # ---- Delete Flight
    def show_delete_flight(self):
        self.clear_content()
        self.styled_title("Delete Flight")

        form_frame = Frame(self.content_frame, bg="white", bd=2, relief="groove")
        form_frame.pack(pady=20)

        Label(form_frame, text="Source Airport:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        src_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        src_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Destination Airport:", bg="white", fg="#2C3E50",
              font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        dest_entry = Entry(form_frame, width=30, bg="white", bd=2, relief="solid")
        dest_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(form_frame, text="Delete Flight",
               command=lambda: self.delete_flight(src_entry.get(), dest_entry.get()),
               bg="#C0392B", fg="white",
               activebackground="#922B21", activeforeground="white",
               relief="raised", bd=2).grid(row=2, columnspan=2, pady=20)

    def delete_flight(self, src, dest):
        if src and dest:
            result = self.db.delete_flight(src, dest)
            if result == "success":
                Label(self.content_frame, text=f"Flight {src} -> {dest} deleted!", fg="red").pack()
            elif result == "not_found":
                Label(self.content_frame, text=f"Flight {src} -> {dest} does not exist!", fg="red").pack()

    # ---- All Airports ----
    def show_all_airports(self):
        airports_window = Toplevel()
        airports_window.title("All Airports")
        airports_window.geometry("800x600")

        scroll = Scrollbar(airports_window)
        scroll.pack(side=RIGHT, fill=Y)

        airports_text = Text(airports_window, font=("Courier New", 12),
                             bg="#ECF0F1", fg="black", yscrollcommand=scroll.set)
        airports_text.pack(fill=BOTH, expand=True)
        scroll.config(command=airports_text.yview)

        airports = self.db.get_airports()
        if not airports:
            airports_text.insert(END, "No airports found in the database.\n")
        else:
            airports_text.insert(END, "\n" + "=" * 50 + "\n")
            airports_text.insert(END, f"{'Airport Name':<30}\n")
            airports_text.insert(END, "-" * 50 + "\n")
            for airport in airports:
                airports_text.insert(END, f"{airport:<30}\n")
            airports_text.insert(END, "=" * 50 + "\n")

        airports_text.config(state="disabled")

    # ---- All Flights ----
    def show_all_flights(self):
        flights_window = Toplevel()
        flights_window.title("All Flights")
        flights_window.geometry("800x600")

        scroll = Scrollbar(flights_window)
        scroll.pack(side=RIGHT, fill=Y)

        flights_text = Text(flights_window, font=("Courier New", 12),
                            bg="#ECF0F1", fg="black", yscrollcommand=scroll.set)
        flights_text.pack(fill=BOTH, expand=True)
        scroll.config(command=flights_text.yview)

        flights = self.db.get_flights()
        if not flights:
            flights_text.insert(END, "No flights found in the database.\n")
        else:
            flights_text.insert(END, "\n" + "=" * 60 + "\n")
            flights_text.insert(END, f"{'Source':<20}{'Destination':<20}{'Cost':<10}\n")
            flights_text.insert(END, "-" * 60 + "\n")
            for src, dest, cost in flights:
                flights_text.insert(END, f"{src:<20}{dest:<20}${cost:<10.2f}\n")
            flights_text.insert(END, "=" * 60 + "\n")

        flights_text.config(state="disabled")

    def run(self):
        """Run the application."""
        self.root.mainloop()
