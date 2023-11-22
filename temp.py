import pandas as pd
import tkinter as tk
from tkinter import ttk

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('your_file.csv')

def create_table(root, dataframe):
    # Create a tkinter window
    window = tk.Toplevel(root)
    window.title("CSV Data")

    # Create a Treeview widget
    tree = ttk.Treeview(window, selectmode='browse')

    # Define columns
    tree["columns"] = tuple(dataframe.columns)
    tree["show"] = "headings"

    # Add columns to the Treeview
    for column in dataframe.columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)  # Adjust the width as needed

    # Insert data into the table
    for index, row in dataframe.iterrows():
        tree.insert("", tk.END, values=tuple(row))

    # Add scrollbar
    scroll_y = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    scroll_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scroll_y.set)

    # Pack the Treeview
    tree.pack(expand=True, fill="both")

    # Function to update the DataFrame when a cell is edited
    def on_cell_edit(event):
        # Get the selected item and column
        selected_item = tree.selection()[0]
        column = tree.identify_column(event.x)
        col_index = tree["columns"].index(column)

        # Get the new value
        new_value = tree.item(selected_item, option="values")[col_index]

        # Update the DataFrame with the new value
        dataframe.at[selected_item, column] = new_value

    # Bind cell editing event to update DataFrame
    tree.bind("<Double-1>", on_cell_edit)

    # Save changes button
    def save_changes():
        # Write the updated DataFrame back to a CSV file
        dataframe.to_csv('updated_file.csv', index=False)
        tk.messagebox.showinfo("Success", "Changes saved to updated_file.csv")

    save_button = tk.Button(window, text="Save Changes", command=save_changes)
    save_button.pack()

# Create the tkinter window
root = tk.Tk()
root.title("CSV Data Viewer")

# Assuming you want to display the data on a button click
button = tk.Button(root, text="Show Data", command=lambda: create_table(root, data))
button.pack()

root.mainloop()