from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
      raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_email", methods=["POST"])
def process_email():
    email_text = request.form.get("email_text", "")
    
    if not email_text.strip():
        return jsonify({"error": "Email text is empty"}), 400
    
    try:
        # Generate summary
        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful email assistant. Summarize this email in 3-5 concise bullet points."},
                {"role": "user", "content": email_text}
            ]
        ).choices[0].message['content']
        
        # Generate reply
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful email assistant. Draft a professional reply to this email."},
                {"role": "user", "content": email_text}
            ]
        ).choices[0].message['content']
        
        return jsonify({
            "summary": summary,
            "reply": reply
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
