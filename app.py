import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import io
import markdown2

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Configure OpenAI API
#openai.api_key = os.getenv("OPENAI_API_KEY")

# File upload configuration
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        flash(f"Error extracting text from PDF: {str(e)}")
        return ""

def tailor_resume(resume_text, job_description):
    """Use OpenAI API to tailor the resume based on the job description"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create a prompt for the OpenAI API
        prompt = f"""
        You are a professional resume writer. Your task is to tailor the provided resume to better match the job description.
        
        Here is the original resume:
        {resume_text}
        
        Here is the job description:
        {job_description}
        
        Please rewrite the resume to highlight relevant skills and experiences that match the job description.
        Focus on:
        1. Matching keywords from the job description
        2. Highlighting relevant experience and skills
        3. Quantifying achievements where possible
        4. Maintaining a professional tone
        5. Keeping the same basic structure as the original resume
        
        Format the tailored resume in Markdown. Use appropriate headings, bullet points, and formatting.
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(            
            model="gpt-4o-mini",  # Use GPT-4 for better quality
            messages=[
                {"role": "system", "content": "You are a professional resume writer who tailors resumes to match job descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        # Extract the tailored resume from the response
        tailored_resume = response.choices[0].message.content
        return tailored_resume
    except Exception as e:
        flash(f"Error tailoring resume: {str(e)}")
        return None

@app.route('/tools/resume-tailor')
def index():
    """Render the landing page"""
    return render_template('index.html')

@app.route('/tools/resume-tailor/dashboard')
def dashboard():
    """Render the resume tailoring tool page"""
    return render_template('tool.html')

@app.route('/tools/resume-tailor/process', methods=['POST'])
def process():
    """Process the resume and job description"""
    # Check if the post request has any files or text
    if not request.files and not request.form:
        flash('No files or text provided')
        return redirect(url_for('dashboard'))
    
    # Get resume content (either from file or text input)
    resume_text = ""
    if 'resume_file' in request.files and request.files['resume_file'].filename:
        resume_file = request.files['resume_file']
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(file_path)
            
            # Extract text based on file type
            if filename.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    resume_text = extract_text_from_pdf(f)
            else:  # .txt file
                with open(file_path, 'r', encoding='utf-8') as f:
                    resume_text = f.read()
                    
            # Clean up the temporary file
            os.remove(file_path)
        else:
            flash('Invalid resume file format. Please upload a PDF or TXT file.')
            return redirect(url_for('dashboard'))
    elif request.form.get('resume_text'):
        resume_text = request.form.get('resume_text')
    else:
        flash('Please provide your resume (either upload a file or paste text)')
        return redirect(url_for('dashboard'))
    
    # Get job description content (either from file or text input)
    job_description = ""
    if 'job_description_file' in request.files and request.files['job_description_file'].filename:
        job_file = request.files['job_description_file']
        if job_file and allowed_file(job_file.filename):
            filename = secure_filename(job_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            job_file.save(file_path)
            
            # Extract text based on file type
            if filename.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    job_description = extract_text_from_pdf(f)
            else:  # .txt file
                with open(file_path, 'r', encoding='utf-8') as f:
                    job_description = f.read()
                    
            # Clean up the temporary file
            os.remove(file_path)
        else:
            flash('Invalid job description file format. Please upload a PDF or TXT file.')
            return redirect(url_for('dashboard'))
    elif request.form.get('job_description_text'):
        job_description = request.form.get('job_description_text')
    else:
        flash('Please provide a job description (either upload a file or paste text)')
        return redirect(url_for('dashboard'))
    
    # Tailor the resume using OpenAI API
    tailored_resume_markdown = tailor_resume(resume_text, job_description)
    
    if not tailored_resume_markdown:
        flash('Failed to tailor resume. Please try again.')
        return redirect(url_for('dashboard'))
    
    # Convert markdown to HTML for display
    tailored_resume_html = markdown2.markdown(tailored_resume_markdown)
    
    # Render the result page
    return render_template('result.html', 
                          tailored_resume_markdown=tailored_resume_markdown,
                          tailored_resume_html=tailored_resume_html)

@app.route('/tools/resume-tailor/export-pdf', methods=['POST'])
def export_pdf():
    """Export the tailored resume as PDF"""
    # This would be implemented with a PDF generation library
    # For now, we'll just redirect back to the result page
    flash('PDF export functionality coming soon!')
    return redirect(url_for('process'))

if __name__ == '__main__':
    # In Docker, we need to listen on 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_ENV') == 'development')
