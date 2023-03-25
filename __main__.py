from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import pandas as pd
import json

window = tk.Tk()
window.title("File Selection")
window.geometry("400x200")

file_path = ''
df = pd.DataFrame()

# This whole functions is needed to transform data
def transforming_data():
        data = []
        df_dict = df.to_dict(orient='records')

        # Dataframe for each item in the dataframe.
        for row in df_dict:
            options_json = row['product_options']
            product_sku = row['product_sku']
            product_name = row['product_name']
            partner_id = row['partner_id']
            partner_name = row['partner_name']
            # This function takes a json string containing options and returns a list of options.
            if isinstance(options_json, str):
                options = json.loads(options_json)
                for option in options:
                    option['partner_id'] = partner_id
                    option['partner_name'] = partner_name
                    option['product_sku'] = product_sku
                    option['product_name'] = product_name
                    category = option['category_name']
                    required = option['required']
                    multiple = option['multiple']
                    max = option['max']
                    sort = option['sort']
                    # Update the data for the items option.
                    if 'items' in option:
                        items = option['items']
                        # Update the items in the list
                        for item in items:
                            item.update({
                                'partner_id': partner_id,
                                'partner_name': partner_name,
                                'product_sku': product_sku,
                                'product_name': product_name,
                                'category_name': category,
                                'required': required,
                                'multiple': multiple,
                                'max': max,
                                'sort': sort,
                            })
                        data.extend(items)
                    option.update({
                        'partner_id': partner_id,
                        'partner_name': partner_name,
                        'product_sku': product_sku,
                        'product_name': product_name,
                        'category_name': category,
                        'required': required,
                        'multiple': multiple,
                        'max': max,
                        'sort': sort,
                    })
                    data.append(option)
        df_normalized = pd.json_normalize(data)
        df_normalized = df_normalized[df_normalized['items'].isnull()].reset_index(drop=True)
        new_sort = ["partner_id", "partner_name", "product_sku", "product_name", "category_name", "name_item", "price", "selected", "required", "multiple", "max", "sort"]
        drop_list = [col for col in df_normalized.columns if col not in new_sort]
        df_normalized.drop(columns=drop_list, inplace=True)
        df_normalized.reindex(columns=new_sort)
        return df_normalized
        
# Select the CSV to transform
def select_and_load_file():
    global file_path
    global df
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Success", "DataFrame loaded successfully!")

# Save results to file
def save_file():
    if not df.empty:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            transforming_data().to_csv(file_path, index=False)
            messagebox.showinfo("Congrats!", f"Result saved at: {file_path}")
    else:
         messagebox.showerror("Error", "No file loaded yet.")

# Show results into a spreadsheet
def show_result():
    if not df.empty:
        scrollbar_y = ttk.Scrollbar(output_frame, orient="vertical")
        scrollbar_x = ttk.Scrollbar(output_frame, orient="horizontal")
        tree = ttk.Treeview(output_frame, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        columns = list(transforming_data().columns)
        tree["columns"] = columns

        for col in columns:
            tree.column(col, width=100, anchor=tk.CENTER)
            tree.heading(col, text=col)

        rows = transforming_data().to_numpy().tolist()

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
        window.update()
        window.geometry(f"{window.winfo_reqwidth()}x{window.winfo_reqheight()}")

    else:
        messagebox.showerror("Error", "No file loaded yet.")

# UI
button_load = ttk.Button(window, text="Load File", command=select_and_load_file)
button_load.pack(pady=10)

button_save = ttk.Button(window, text="Save File", command=save_file)
button_save.pack(pady=10)

button_result = ttk.Button(window, text="Show Result", command=show_result)
button_result.pack(pady=10)

style = ttk.Style()

style.theme_use('clam')
style.configure("My.TLabelframe", background="#f0f0f0")

output_frame = ttk.LabelFrame(window, text="Result", padding=(10, 10, 10, 10), style="My.TLabelframe")
output_frame.pack(padx=20, pady=20, fill="both", expand=True)

style.configure("My.Treeview", background="white", foreground="black", rowheight=25)

tree = ttk.Treeview(output_frame, style="My.Treeview")

window.mainloop()


## Created by: _shrpp [lucius.2906@gmail.com]