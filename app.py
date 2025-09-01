import os
import sqlite3
import markdown
from datetime import datetime
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies

# Import your custom utility functions
from utils.gemini import gemini_generate_summary
from utils.extract import extract_text_from_url, extract_text_from_pdf
from utils.image import extract_image_from_url
from utils.pdf import generate_pdf


# Import LangChain components
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter


# --- App Initialization ---
load_dotenv()
app = Flask(__name__)

# --- Configurations ---
app.config["SECRET_KEY"] = "your-flask-secret-key"
app.config["JWT_SECRET_KEY"] = "your-super-secret-key-change-me"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Store JWTs in cookies
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

jwt = JWTManager(app)
# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    # Create users table if not exists (assuming you have one)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    # Create history table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            topic TEXT,
            summary TEXT,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Authentication Routes ---
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        # First, find the user by their username
        c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
        user = c.fetchone() # Fetches one record or None
        conn.close()

        # The user's password is the 3rd item in the tuple (index 2)
        # Check if the user was found AND if the password matches
        if user and password == user[2]:
            # --- SUCCESS ---
            access_token = create_access_token(identity=username)
            response = redirect(url_for("dashboard"))
            set_access_cookies(response, access_token)
            session["username"] = username  # For display purposes
            return response
        else:
            # --- FAILURE ---
            flash("Invalid username or password.", "danger")
            return render_template("login.html")
            
    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    # In a full JWT app, you'd also unset the cookie, but redirecting is fine here.
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# --- Core Application Routes ---
@app.route("/dashboard")
@jwt_required()
def dashboard():
    return render_template("dashboard.html")

@app.route("/process", methods=["POST"])
@jwt_required()
def process():
    current_user = get_jwt_identity()
    input_type = request.form.get("input_type")
    # --- NEW: Get the chosen summary style from the form ---
    summary_style = request.form.get("summary_style", "detailed") # Default to 'detailed'

    print(f"DEBUG: Form data received by process route: {request.form}")
    current_user = get_jwt_identity()
    input_type = request.form.get("input_type")
    user_topic = None
    summary = ""
    image_path = None
    new_id = None
    
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            flash("Google API key not found. Please set it in your .env file.", "danger")
            return redirect(url_for("dashboard"))
        
        detailed_prompt_template = """
        Your task is to generate a comprehensive summary structured primarily with detailed bullet points...
        {text_to_summarize}
        """ # Using the detailed prompt we created
       
        # Select the chosen prompt template
    

        # --- Logic for Topic, URL, and PDF ---
        if input_type == "topic":
            user_topic = request.form.get("topic")
            # ... (rest of the logic)
            final_prompt = detailed_prompt_template.format(text_to_summarize=f"The topic of: {user_topic}")
            summary = gemini_generate_summary(final_prompt,api_key)
        
        elif input_type == "url":
            url = request.form.get("url")
            user_topic = f"URL: {url}"
            content = extract_text_from_url(url)
            content = content[:16000]
            final_prompt = detailed_prompt_template.format(text_to_summarize=content)
            summary = gemini_generate_summary(final_prompt, api_key)
            image_path = extract_image_from_url(url) 

        elif input_type == "pdf":
            # ... (your full PDF logic here)
            file = request.files.get("file")
            filename = secure_filename(file.filename)
            user_topic = f"PDF: {filename}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            content = extract_text_from_pdf(filepath)
            MAX_CHARS = 16000
            content = content[:MAX_CHARS]
            final_prompt = detailed_prompt_template.format(text_to_summarize=content)
            summary = gemini_generate_summary(final_prompt,api_key)

        else:
            flash("Invalid submission type.", "danger")
            return redirect(url_for("dashboard"))
        
        # --- Save to Database ---
       
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO history (username, topic, summary, image_path, timestamp) VALUES (?, ?, ?, ?, ?)",
            (current_user, user_topic, summary, image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        new_id = c.lastrowid
        conn.close()

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for("dashboard"))
    
    return render_template("dashboard.html", summary=markdown.markdown(summary), image_url=image_path, new_history_id=new_id,result_type=input_type)

# In app.py, add this function after your 'process' function

@app.route("/ask", methods=["POST"])
@jwt_required()
def ask():
    current_user = get_jwt_identity()
    question = request.form.get("question")
    
    # Get the temperature from the form, defaulting to 0.7 for more creative answers
    temperature = float(request.form.get("temperature", 0.7))

    if not question:
        flash("Please ask a question.", "danger")
        return redirect(url_for("dashboard"))

    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            flash("Google API key not found.", "danger")
            return redirect(url_for("dashboard"))

        # A simple prompt that tells the AI to be a helpful assistant
        prompt_text = f"Please provide a helpful and comprehensive answer to the following question:\n\nQuestion: {question}\n\nAnswer:"
        
        # We reuse our existing gemini function, but pass the new prompt and temperature
        answer = gemini_generate_summary(prompt_text, api_key, temperature)

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for("dashboard"))
    
    # We render the dashboard, passing the answer to a new variable
    return render_template("dashboard.html", ask_anything_answer=markdown.markdown(answer), result_type='ask')


@app.route("/chat_pdf", methods=["POST"])
@jwt_required()
def chat_pdf():
    current_user = get_jwt_identity()
    file = request.files.get("pdf_file")
    question = request.form.get("question")

    if not file or not question:
        flash("Please upload a file and ask a question.", "danger")
        return redirect(url_for("dashboard"))

    try:
        # --- FIX: Load the API Key ---
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            flash("Google API key not found. Please set it in your .env file.", "danger")
            return redirect(url_for("dashboard"))

        # 1. Load PDF
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        loader = PyPDFLoader(filepath)
        pages = loader.load_and_split()

        # 2. Split into smaller chunks
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )
        docs = text_splitter.split_documents(pages)

        # 3. Create embeddings + vector store
        # --- FIX: Pass the API Key ---
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        vector_store = FAISS.from_documents(docs, embedding=embeddings)

        # ... (rest of the function is the same) ...

        # 5. Define prompt
        prompt_template = """
        Answer the question based only on the provided context.
        Context: {context}
        Question: {question}
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # 6. Build chain
        # --- FIX: Pass the API Key ---
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3, google_api_key=api_key)
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        # 7. Run QA chain
        relevant_docs = vector_store.similarity_search(question)
        response = chain(
            {"input_documents": relevant_docs, "question": question},
            return_only_outputs=True
        )

        return render_template("dashboard.html", chat_answer=markdown.markdown(response["output_text"]),result_type='chat')

    except Exception as e:
        # Provide a more specific error message
        flash(f"An error occurred during PDF chat: {e}", "danger")
        return redirect(url_for("dashboard"))
@app.route("/history")
@jwt_required()
def history():
    current_user = get_jwt_identity()
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute(
        "SELECT id, topic, summary, image_path, timestamp FROM history WHERE username=? ORDER BY id DESC", 
        (current_user,)
    )
    raw_records = c.fetchall()
    conn.close()

    processed_records = []
    for record in raw_records:
        processed_record = dict(record)
        if processed_record['summary']:
            processed_record['summary'] = markdown.markdown(processed_record['summary'])
        processed_records.append(processed_record)

    return render_template("history.html", history_records=processed_records)

@app.route("/download/<int:history_id>")
@jwt_required()
def download(history_id):
    current_user = get_jwt_identity()
    conn = sqlite3.connect("database.db")
    c = conn.cursor() 
    c.execute("SELECT summary, image_path FROM history WHERE id=? AND username=?", (history_id, current_user))
    row = c.fetchone()
    conn.close()

    if not row:
        flash("Record not found", "danger")
        return redirect(url_for("history"))

    summary_text, image_path = row
    pdf_path = generate_pdf(summary_text, image_path)
    return send_file(pdf_path, as_attachment=True)
print(app.url_map)
# --- Main Execution ---
if __name__ == "__main__":
    app.run(debug=True)