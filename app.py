from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from pdf import create_pdf
import markdown

app = Flask(__name__)

genai.configure(api_key="AIzaSyC1os1sad3RodhDfoiFd989mR9KANnSjo")

generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
    system_instruction="task to create structured audit report based on given data.",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "model",
      "parts": [
        "Hello! I am a chatbot made to help you create a structured audit report. Please share the audit data.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "hello",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Hello!  I'm ready to help you.  Please provide me with the data for the audit report you'd like me to generate.  I need information such as the purpose of the audit, its scope, the period covered, the findings (with descriptions, locations, impacts, and recommendations), and overall conclusions.  The more detail you give me, the better the report will be.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "note: do not use table. you can use numbering and formatting. provide report in detail.",
      ]
    }
  ]
)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['message']
    response = chat_session.send_message(user_message)
    response_text = markdown.markdown(response.text)
    pdf_file_path = None
    if len(user_message) > 1600:
        create_pdf(response.text)
        pdf_file_path = "./audit_report.pdf"
    return jsonify({
        'response': response_text,
        'pdf_file': pdf_file_path})

if __name__ == '__main__':
    app.run(debug=False)
