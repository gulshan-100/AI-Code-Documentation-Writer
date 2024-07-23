from dotenv import load_dotenv, find_dotenv
import os
from flask import Flask, request, render_template, flash
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import markdown

load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0.7)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['codeInput']
        if not content.strip():
            flash('Please enter some code before submitting.', 'error')
            return render_template('index.html')
        
        try:
            template = """
                Generate comprehensive documentation for the provided code snippet. 
                User should be able to understand complete code snippet in easy way. 
                Code Snippet:
                {code}
                """
            prompt = PromptTemplate(
                input_variables=['code'],
                template=template
            )

            response = llm.invoke(prompt.format(code=content)).content
            
            # Convert Markdown to HTML
            html_content = markdown.markdown(response)
            
            return render_template('index.html', documentation=html_content, code=content)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return render_template('index.html', code=content)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)