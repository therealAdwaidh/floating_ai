<img width="1270" height="730" alt="image" src="https://github.com/user-attachments/assets/088b9565-2cff-4087-be1b-f09209b9c105" />

Floating AI — Your Smart Desktop Chat with Memory

Floating AI is a simple desktop app built with Python + PyQt5 that lets you chat with an AI assistant, save important notes, and revisit past conversations anytime. You can quickly recall, manage, or clear memory and history with ease. Lightweight and efficient, it’s designed for speed and simplicity.

---

 Features

* AI Chat Interface — Type messages and get instant AI responses.
* Markdown Output — Supports formatted text, code blocks, and lists.
* Persistent Memory — Save important notes automatically or on command.
* Memory Management

  * `memory` → Displays all saved notes.
  * `clear memory` → Deletes all saved notes.

* Conversation History

  * `history` → Displays your past conversations.
  * `clear history` → Erases conversation logs.
  
* Model Selection — Choose from multiple AI models using the dropdown before sending a query.
* Clipboard Copy — Press the Copy Output button to copy AI responses instantly.
* Custom Personality — Use `set personality: ...` to adjust AI behavior.
* Minimalist UI — Focus on chatting without distractions.
* Automatic Memory Saving — Important notes are saved automatically when you type keywords like `remember`, `note`, `important`, `save`, or `store`.
* Clear All — Use `clear all` to delete both conversation history and memory.

---

Installation

1. Clone the repository

```bash
git clone https://github.com/therealAdwaidh/floating_ai.git
cd floating-ai


2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

#bash
python main.py


---

Project Structure


floating-ai/
│
├── features/               # Feature files
│
├── history.txt             # Conversation history
├── memory.txt              # Saved important notes
├── personality.txt         # Personality settings
│
├── Client.py               # AI backend interface
├── main.py                 # Main PyQt5 application
├── requirements.txt        # Dependencies
└── README.md               # This file


---

 Commands Reference

| Command              | Action                                      |
| -------------------- | ------------------------------------------- |
| `exit`               | Close the app                               |
| `clear`              | Clear the current output                    |
| `history`            | Show conversation history                   |
| `clear history`      | Erase all conversation history              |
| `memory`             | Show everything saved in `memory.txt`       |
| `clear memory`       | Delete everything inside `memory.txt`       |
| `set personality: …` | Save personality settings for the AI        |
| `clear all`          | Delete both conversation history and memory |



 Copying Responses

Every AI response includes a Copy Output button. Click it to instantly copy the output to your clipboard — perfect for sharing code snippets, notes, or answers.



 Requirements

* Python 3.8+
* PyQt5
* markdown

Install all requirements with:

bash
pip install -r requirements.txt


---

 License

MIT License — free to modify and distribute.

---

 Credits


* PyQt5 for UI
* Markdown for rendering responses
* AI magic courtesy of your favorite LLM API
* Model selection integration for multiple AI backends



