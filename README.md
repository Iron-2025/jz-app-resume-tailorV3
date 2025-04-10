# Resume Tailor

Resume Tailor is a web application that helps users customize their resumes based on job descriptions using AI. The application analyzes the job description and the user's resume to highlight relevant skills and experiences, increasing the chances of getting interviews.

## Features

- Upload or paste resume content (PDF or TXT format)
- Upload or paste job description (PDF or TXT format)
- AI-powered resume tailoring using OpenAI's GPT-4
- Export tailored resume as Markdown
- Copy tailored resume to clipboard
- Responsive design for all devices

## Screenshots

![Landing Page](static/img/resume-illustration.svg)

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Tailwind CSS
- **AI**: OpenAI GPT-4
- **PDF Processing**: PyPDF2

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/resume-tailor.git
   cd resume-tailor
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   # Copy the example file
   cp .env.example .env
   
   # Edit the .env file and add your OpenAI API key
   # OPENAI_API_KEY=your_openai_api_key_here
   # SECRET_KEY=your_secret_key_here
   ```

## Usage

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Upload or paste your resume and the job description you're applying for.

4. Click "Tailor My Resume" and wait for the AI to process your resume.

5. View, copy, or download your tailored resume.

## Development

### Project Structure

```
resume-tailor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # Project documentation
├── static/                # Static files
│   ├── css/               # CSS styles
│   ├── js/                # JavaScript files
│   └── img/               # Images
└── templates/             # HTML templates
    ├── index.html         # Landing page
    ├── tool.html          # Resume tailoring tool
    └── result.html        # Results page
```

### Adding New Features

1. **PDF Export**: Implement PDF generation using a library like WeasyPrint or pdfkit.
2. **User Accounts**: Add user authentication to save tailored resumes.
3. **Multiple Resume Versions**: Allow users to save multiple versions of tailored resumes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for providing the GPT-4 API
- Tailwind CSS for the styling framework
