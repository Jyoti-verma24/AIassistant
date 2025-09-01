AI Research Assistant & Prompt Engineering Training Tool
Overview
This is a comprehensive, Flask-based web application designed to be a powerful tool for AI-driven research and prompt engineering. Powered by Google's Gemini AI through the LangChain framework, this application allows users to generate, analyze, and interact with content from various sources, including general topics, web articles, PDFs, and even YouTube videos.

The project serves as a practical demonstration of modern AI integration, featuring user authentication, a dynamic user interface, and multiple advanced features that allow users to control and refine AI-generated content.

Key Features
This project is packed with a wide range of advanced features:

Ask Me Anything: A general-purpose chatbot that can answer any question, complete with a voice-to-text input option.

Multi-Source Summarization: Generate detailed summaries from:

General Topics: Any subject you can think of.

Web Articles: Provide a URL to get a summary and extract the main image.

PDF Documents: Upload a PDF file for analysis.

YouTube Videos: Simply provide a YouTube link to get a summary of the video's transcript.

Interactive AI Controls:

Creativity Slider (Temperature): A slider on each form allows you to control the AI's "creativity," from highly factual (low temperature) to more imaginative and fluent (high temperature).

Intelligent Image Extraction: When summarizing a URL, the application intelligently scrapes the webpage to find and display the most relevant content image.

Interactive PDF Chat: Upload a PDF and ask specific questions about its content.

Text-to-Speech: An accessible "Read Aloud / Stop" button appears next to every generated summary or answer, allowing the AI's response to be read out loud.

Full User Authentication: Secure user registration and login system using JWT (JSON Web Tokens) stored in cookies.

Search History: All generated summaries and images are saved to a user-specific history page for later review.

Download as PDF: Any generated summary can be downloaded as a cleanly formatted PDF document.

Technologies Used
Backend: Python, Flask, Gunicorn

Frontend: HTML, CSS, Bootstrap 5

Database: SQLite

AI & Machine Learning:

LangChain

Google Generative AI (Gemini)

Other Key Libraries:

Flask-JWT-Extended for authentication.

youtube-transcript-api for fetching video transcripts.

BeautifulSoup4 for web scraping.

PyMuPDF for PDF text extraction.

Setup and Installation
To run this project locally, please follow these steps:

Clone the Repository:

git clone https://github.com/Jyoti-verma24/AIassistant.git
Create and Activate a Virtual Environment:

# For Windows
python -m venv venv
venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Create a .env File:
Create a file named .env in the root of the project folder and add your API keys and secret keys:

GOOGLE_API_KEY="your_google_api_key_here"
SECRET_KEY="a_very_strong_random_secret_key"
JWT_SECRET_KEY="another_very_strong_random_secret_key"

Run the Application:

python app.py

The application will be running at http://127.0.0.1:5000.

How to Use
Register: Create a new user account.

Login: Log in with your new credentials.

Use the Tools: You will be redirected to the main dashboard where you can use any of the features.

Check History: Click on the "History" tab in the sidebar to see all your past generations.