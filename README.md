🤖 AI Research Assistant & Prompt Engineering Tool

A powerful, multi-featured web application built with Flask and powered by Google's Gemini AI. This tool allows users to summarize content from various sources, interact with documents, and experiment with AI behavior in real-time.

✨ Key Features
This project is a comprehensive suite of AI tools designed for research and learning:

General Purpose AI Chat
Ask Me Anything: A fully functional chatbot that can answer general knowledge questions, complete with a voice-to-text option using the microphone.

Multi-Source Summarization
Topic Summarizer: Generate a detailed summary on any subject.

URL Summarizer: Provide a link to any web article to get a summary and automatically extract the main content image.

PDF Summarizer: Upload a PDF document for a complete summary.

Advanced AI & Prompt Engineering Controls
Creativity Slider (Temperature Control): A slider is included on every form, allowing you to directly control the AI's "creativity." A low temperature produces factual, predictable text, while a high temperature results in more imaginative and fluent responses.

Interactive Tools & User Experience
Chat with PDF: Upload a PDF document and ask specific questions about its contents. The AI will answer based only on the information in the document.

"Read Aloud" with Stop Button: Every generated summary and answer includes an accessible "Read Aloud" button that transforms into a "Stop" button, allowing for easy text-to-speech functionality.

"AI is Thinking..." Indicator: A professional loading spinner appears after submitting any request, providing clear feedback that the AI is processing in the background.

Full User Authentication: Secure registration and login system using JWT, with a dedicated history page for each user to review past results.

Download as PDF: Any generated summary can be downloaded as a cleanly formatted PDF document.

💻 Technologies Used

Backend: Python, Flask, Gunicorn
Frontend: HTML, CSS, Bootstrap 5
Database: SQLite
AI & Machine Learning:
LangChain
Google Generative AI (Gemini)

Key Python Libraries:
Flask-JWT-Extended
youtube-transcript-api & pytube
BeautifulSoup4 & requests
PyMuPDF

