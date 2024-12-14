import os
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, font

file_path = r"C:\Users\22053345_KIIT\Desktop\Olympics Chatbot\olympics2024.csv"

if not os.path.exists(file_path):
    print("File does not exist:", file_path)
else:
    def load_medal_data(file_path):
        try:
            df = pd.read_csv(file_path)  
            olympics2024 = {}
            for index, row in df.iterrows():
                country = row['Country'].strip().lower()  
                olympics2024[country] = {
                    "Gold": row['Gold'],
                    "Silver": row['Silver'],
                    "Bronze": row['Bronze'],
                    "Total": row['Total']
                }
            return olympics2024
        except Exception as e:
            print(f"Error loading medal data: {e}")
            return {}

    def get_bot_response(user_input, olympics2024):
        user_input = user_input.lower()

        for country in olympics2024:
            if country in user_input:
                medals = olympics2024[country]
                return (f"{country.title()} has won {medals['Gold']} Gold, {medals['Silver']} Silver, "
                        f"and {medals['Bronze']} Bronze medals, totaling {medals['Total']} medals.")
        
        if "hello" in user_input:
            return "Hello! How can I help you today?"
        elif "olympics" in user_input:
            return "The Olympics are a global event featuring summer and winter sports."
        elif "Medals History" in user_input:
            return "Please specify the country you're interested in."
        else:
            return "I'm not sure how to respond to that."

    def send_message():
        user_input = entry_box.get("1.0", "end-1c").strip()  
        entry_box.delete("1.0", "end")  

        if user_input:
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, "You: " + user_input + "\n")
            bot_response = get_bot_response(user_input, olympics2024)
            chat_area.insert(tk.END, "Bot: " + bot_response + "\n")
            chat_area.config(state=tk.DISABLED)
            chat_area.yview(tk.END)  

    root = tk.Tk()
    root.title("Olympic Chatbot")
    root.geometry("500x550")
    root.configure(bg="#ffffff")  # White background for the window

    # Create the chat area with Olympic-themed colors
    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#f0f8ff", fg="#000000", font=("Helvetica", 12))
    chat_area.config(state=tk.DISABLED)
    chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create the entry box
    entry_box = tk.Text(root, height=3, bg="#e6f7ff", fg="#000000", font=("Helvetica", 12))
    entry_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

    # Create the send button with Olympic colors
    send_button = tk.Button(root, text="Send", command=send_message, bg="#ffcc00", fg="#000000", font=("Helvetica", 12, "bold"))
    send_button.pack(padx=10, pady=10)

    # Load the medal data from the CSV file
    olympics2024 = load_medal_data(file_path)
    print(olympics2024)

    root.mainloop()
