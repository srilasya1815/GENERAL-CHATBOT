📚 General Chatbot Project

This is a simple general-purpose chatbot built using Flask, TOGETHREAI API, and a web interface.
It can answer questions on any topic using DEEPSEEK-Llema , and also responds to predefined patterns from intents.json.


---

🚀 Features

User-friendly web interface

Responds using TOGETHREAI API

Predefined intents & responses for quick replies

Chat history saved in chat_history.json

Option to clear chat history



---

🛠 Setup Instructions

1️⃣ Clone the Repository

git clone <your-github-repo-link>
cd chatbot-project

2️⃣ Create Virtual Environment (optional but recommended)

python -m venv venv
venv\Scripts\activate       
3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Your TOGETHREAI API  Key

In app.py, replace this line:

openai.api_key = "your-api-key-here"

with your actual  TOGETHREAI API key.
(Or better: set it as an environment variable and load it in the code for security.)


---

📄 How to Run

python app.py

Then open your browser and go to:
👉 http://127.0.0.1:5000


---

💬 How to Use

Type your message in the chat box and press send.

If your message matches a pattern in intents.json, it will reply from there.

Otherwise, it queries the OpenAI API for a response.

Chat history is saved in chat_history.json.

Use the "Clear History" button (if added) to delete past chats.



---

📁 Files & Structure

chatbot-project/
├── app.py                        
├── chat_history.json    
├── requirements.txt     
├── README.md            
└── templates/
    └── index.html       


---

📷 Demo Video

🎥 YouTube link to project explanation video
(Replace # with your actual YouTube link once uploaded.)


---

🌟 Credits & Resources

TOGETHREAI API Documentation

Flask Documentation

W3Schools Tutorials
