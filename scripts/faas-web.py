import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import pickle
import os
import requests

class FaaSWebDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("FaaS Web")
        self.root.geometry("600x600")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.insert(0, "http://localhost:8080")
        self.url_entry.pack(pady=5)

        tk.Label(self.root, text="Paste JSON here:").pack(pady=5)
        self.json_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.json_text.pack(pady=5)

        send_button = tk.Button(self.root, text="Send Request", command=self.send_request)
        send_button.pack(pady=10)

        tk.Label(self.root, text="Response:").pack(pady=5)
        self.response_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.response_text.pack(pady=5)

    def send_request(self):
        url = self.url_entry.get()
        json_input = self.json_text.get("1.0", tk.END).strip()

        if not url or not json_input:
            messagebox.showerror("Error", "All fields are required. Please fill in all fields.")
            return

        try:
            json_data = json.loads(json_input)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON. Please check the format.")
            return

        data = {
            "action": "",
            "input": json_data
        }

        file_path = os.path.join('/tmp', 'data.pkl')
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)

        try:
            response = requests.post(url, data=open(file_path, 'rb'), headers={'Content-Type': 'application/octet-stream'})
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Request response:\n{response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error sending request: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaaSWebDesktop(root)
    root.mainloop()
