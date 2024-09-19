import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import pickle
import os
import requests


class FaaSDesktopClient:
    OPENFAAS_URL = "http://localhost:8080"

    def __init__(self, root):
        self.root = root
        self.root.title("FaaS Desktop Client")
        self.root.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        self.create_url_input()
        self.create_function_name_input()
        self.create_body_input()
        self.create_send_button()
        self.create_response_output()

    def create_url_input(self):
        tk.Label(self.root, text="URL:").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.insert(0, self.OPENFAAS_URL)
        self.url_entry.pack(pady=5)

    def create_function_name_input(self):
        tk.Label(self.root, text="Function Name:").pack(pady=5)
        self.function_name_entry = tk.Entry(self.root, width=50)
        self.function_name_entry.pack(pady=5)

    def create_body_input(self):
        tk.Label(self.root, text="Paste the body here:").pack(pady=5)
        self.json_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.json_text.pack(pady=5)
        self.json_text.insert(tk.END, "{}")

    def create_send_button(self):
        send_button = tk.Button(
            self.root,
            text="Send Request",
            command=self.send_request,
        )
        send_button.pack(pady=10)

    def create_response_output(self):
        tk.Label(self.root, text="Response:").pack(pady=5)
        self.response_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.response_text.pack(pady=5)
        self.response_text.config(state=tk.DISABLED)

    def send_request(self):
        url = self.url_entry.get()
        json_input = self.json_text.get("1.0", tk.END).strip()
        function_name = self.function_name_entry.get()

        if not self.validate_input(url, json_input):
            return

        try:
            json_data = json.loads(json_input)
            data = {"action": function_name, "input": json_data}
            pickled_data = pickle.dumps(data)

            response = requests.post(
                url,
                data=pickled_data,
                headers={"Content-Type": "application/octet-stream"},
            )
            self.display_response(response)
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error sending request: {str(e)}")

    def validate_input(self, url, json_input):
        if not url or not json_input:
            messagebox.showerror(
                "Error",
                "All fields are required. Please fill in all fields.",
            )
            return False
        try:
            json.loads(json_input)
            return True
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON. Please check the format.")
            return False

    def display_response(self, response):
        unpickled_response = pickle.loads(response.content)
        json_response = json.dumps(unpickled_response, indent=2)
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, json_response)
        self.response_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = FaaSDesktopClient(root)
    root.mainloop()
