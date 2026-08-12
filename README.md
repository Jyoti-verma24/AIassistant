# 🤖 AI Research Assistant & Prompt Engineering Tool

A powerful, multi-featured web application built with **Flask** and powered by **Google Gemini AI**. The application provides a collection of AI-powered tools for **research, document analysis, summarization, and prompt experimentation**.

Users can summarize information from different sources, interact with PDF documents, ask questions about uploaded content, control AI creativity using temperature settings, and save their previous results through an authenticated user account.

---

## ✨ Features

### 💬 1. General Purpose AI Chat

**Ask Me Anything** provides a general-purpose AI chatbot capable of answering questions and assisting with various tasks.

* Ask general knowledge questions
* Get AI-generated responses
* Voice-to-text input using the microphone
* Adjustable AI creativity using the temperature slider
* Read AI responses aloud using text-to-speech

---

### 📚 2. Multi-Source Summarization

The application supports summarization from multiple types of sources.

#### 📝 Topic Summarizer

Enter any topic and generate an AI-powered summary.

* Detailed topic summaries
* Adjustable creativity/temperature
* Read generated content aloud
* Download the generated summary as a PDF

#### 🌐 URL Summarizer

Provide a webpage URL and automatically summarize its content.

* Extracts the main article content
* Generates an AI-powered summary
* Automatically extracts the main image from the webpage
* Supports adjustable temperature
* Download results as PDF

#### 📄 PDF Summarizer

Upload a PDF document and generate a complete summary.

* PDF text extraction
* AI-powered summarization
* Supports large research/document files
* Read summary aloud
* Download summary as PDF

---

### 🧠 3. Chat with PDF

Upload a PDF and interact with it using natural language.

Users can ask specific questions about the uploaded document, and the AI generates answers based **only on the information available in the document**.

**Example:**

> Upload a research paper → Ask "What is the methodology used?" → Get an answer based on the paper.

This makes the feature useful for:

* 📑 Research papers
* 📚 Study material
* 📖 Books and notes
* 📄 Technical documentation
* 📝 Reports

---

### 🎛️ 4. AI Creativity Control

The application provides a **Temperature / Creativity Slider** for controlling AI behavior.

| Temperature | Behavior                               |
| ----------- | -------------------------------------- |
| Low         | More factual and predictable responses |
| Medium      | Balanced responses                     |
| High        | More creative and diverse responses    |

This allows users to experiment with **prompt engineering and AI behavior**.

---

### 🔊 5. Read Aloud

Generated answers and summaries include a **Read Aloud** feature using text-to-speech.

* 🔊 Start reading
* ⏹️ Stop reading
* Useful for accessibility
* Helpful when reviewing long documents or summaries

---

### ⏳ 6. AI Processing Indicator

Whenever an AI request is submitted, the application displays an **"AI is Thinking..."** loading indicator.

This provides visual feedback while the AI processes the request and improves the overall user experience.

---

### 🔐 7. User Authentication

The application includes a complete authentication system.

* User registration
* Secure login
* JWT-based authentication
* User-specific history
* Protected application routes

Each user can access their own previous AI-generated results.

---

### 🕘 8. History

Users can review their previous AI interactions from a dedicated history section.

The history system helps users:

* Revisit previous summaries
* Review previous AI responses
* Keep track of research
* Access earlier results

---

### 📥 9. Download Results as PDF

Generated summaries can be downloaded as professionally formatted PDF documents.

This makes it easy to:

* Save research material
* Share summaries
* Print results
* Keep offline copies

---

# 🛠️ Technologies Used

## Backend

* **Python**
* **Flask**
* **Gunicorn**
* **SQLite**

## Frontend

* **HTML5**
* **CSS3**
* **Bootstrap 5**
* **JavaScript**

## AI & Machine Learning

* **Google Gemini AI**
* **LangChain**
* **Google Generative AI**

## Python Libraries

* `Flask-JWT-Extended`
* `youtube-transcript-api`
* `pytube`
* `BeautifulSoup4`
* `requests`
* `PyMuPDF`

---

# 🏗️ Application Workflow

```text
                ┌──────────────────────┐
                │        User          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Flask Web App      │
                └──────────┬───────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Topic Input    URL Input      PDF Upload
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Content Extract │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Gemini AI      │
                  │  + LangChain    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ AI Generated    │
                  │ Response        │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Read Aloud      History      Download PDF
```

# 📂 Project Structure

```text
AI-Research-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── database/
│   └── database.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── chat.html
│   ├── summarizer.html
│   └── history.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── uploads/
```
# 🎯 Use Cases

This application can be useful for:

* 🎓 Students studying research papers
* 🔬 Researchers analyzing documents
* 📚 Students summarizing study material
* 👨‍💻 Developers experimenting with LLMs
* 🧠 Learning prompt engineering
* 📄 Quickly analyzing long PDFs
* 🌐 Summarizing online articles
* 🎤 Hands-free AI interaction

---
This project is developed for **educational, research, and learning purposes**, with a focus on exploring **Generative AI, prompt engineering, document processing, and AI-powered web applications**.
