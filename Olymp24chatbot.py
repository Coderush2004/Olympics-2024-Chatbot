import os
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext, font
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

file_path = r"C:\Users\22053345_KIIT\Desktop\PROJECTS\Olympics Chatbot"

# Check if the file exists
if not os.path.exists(file_path):
    print("File does not exist:", file_path)
else:
    def load_medal_data(file_path):
        try:
            df = pd.read_csv(file_path)
            
            # Check if the required columns exist in the DataFrame
            required_columns = ['Gold', 'Silver', 'Bronze', 'Total']
            for column in required_columns:
                if column not in df.columns:
                    print(f"Error: Column '{column}' is missing from the CSV file")
                    return pd.DataFrame()  # Return an empty DataFrame if any column is missing

            # Optionally, strip any spaces from column names
            df.columns = df.columns.str.strip()

            return df
        except Exception as e:
            print(f"Error loading medal data: {e}")
            return pd.DataFrame()

    def train_linear_regression(df):
        # Select the independent variables (features) and dependent variable (target)
        features = df[['Gold', 'Silver', 'Bronze']]  # Features: Gold, Silver, Bronze
        target = df['Total']  # Target: Total medals

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Initialize and train the linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict on the test data
        y_pred = model.predict(X_test)

        # Evaluate the model using Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error (MSE): {mse}")

        # Return the trained model
        return model

    def predict_medals(model, gold, silver, bronze):
        # Make a prediction using the trained model
        prediction = model.predict([[gold, silver, bronze]])
        return prediction[0]

    def get_bot_response(user_input, olympics2024, model):
        user_input = user_input.lower()

        for country in olympics2024:
            if country in user_input:
                medals = olympics2024[country]
                prediction = predict_medals(model, medals['Gold'], medals['Silver'], medals['Bronze'])
                return (f"{country.title()} has won {medals['Gold']} Gold, {medals['Silver']} Silver, "
                        f"and {medals['Bronze']} Bronze medals, totaling {medals['Total']} medals. "
                        f"Prediction of total medals in the next Olympics: {prediction:.2f}.")
        
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
            bot_response = get_bot_response(user_input, Olymp24chatbot, model)
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
    df = load_medal_data(file_path)

    # If the required columns are missing, do not proceed
    if not df.empty:
        # Train the linear regression model
        model = train_linear_regression(df)
    else:
        print("Cannot proceed without the required columns.")

    root.mainloop()
