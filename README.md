# 🤖 Agentic Form Filling AI

An intelligent, AI-powered form automation tool that automatically detects and fills web forms, PDF forms, and other application forms using artificial intelligence.

## Features

✨ **Core Features:**
- 🔍 **Smart Form Detection** - Automatically detects form fields (text, email, dropdowns, checkboxes, etc.)
- 🤖 **AI-Powered Suggestions** - Uses OpenAI GPT-4 or Google Gemini to intelligently suggest appropriate data
- 🌐 **Web Form Automation** - Automatically fills web forms using Selenium/Playwright
- 📄 **PDF Form Support** - Extract data from PDF files and fill PDF forms
- 📊 **Multi-Source Data Extraction** - Extract from documents, CSVs, JSON, databases
- ✅ **Smart Validation** - Validates data before filling (email, phone, dates, etc.)
- 🔄 **Auto-Submit** - Optional automatic form submission
- 🎯 **Field Mapping** - Intelligent mapping between user data and form fields

## Technology Stack

### Backend
- **Python 3.10+** with FastAPI
- **Selenium & Playwright** for browser automation
- **OpenAI GPT-4 / Google Gemini** for AI intelligence
- **SQLAlchemy** for database management
- **pdfplumber & PyPDF2** for PDF handling

### Frontend
- **React 18** with Hooks
- **Axios** for API communication
- **Modern CSS3** styling

### Supported Browsers
- Chrome/Chromium
- Firefox
- Microsoft Edge

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- ChromeDriver (for Selenium)

### Backend Setup

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

5. **Download ChromeDriver** (if not installed)
   - Download from: https://chromedriver.chromium.org/
   - Add to PATH or specify in configuration

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

## Usage

### Starting the Backend

**Windows:**
```bash
cd backend
run.bat
```

**Linux/Mac:**
```bash
cd backend
bash run.sh
```

Or manually:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Starting the Frontend

```bash
cd frontend
npm start
```

The application will open at `http://localhost:3000`

## API Endpoints

### Form Detection
```
GET /api/forms/detect?url=<website_url>
```
Detects all forms on a given webpage.

### Form Filling
```
POST /api/forms/fill
Body: {
  "url": "https://example.com/form",
  "form_data": {"field_name": "value"},
  "field_mappings": {"field_name": "#css-selector"},
  "submit_form": true
}
```

### Data Extraction
```
POST /api/extract/pdf
POST /api/extract/text
POST /api/extract/json
POST /api/extract/csv
```

### AI Analysis
```
GET /api/automation/validate-data?field_type=email&value=test@example.com
```

### Smart Auto-Fill
```
POST /api/automation/smart-fill
Body: {
  "url": "https://example.com/form",
  "user_data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  }
}
```

## Configuration

Create a `.env` file in the backend directory:

```env
# AI Configuration
AI_PROVIDER=openai  # or gemini
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
AI_MODEL=gpt-4

# Browser Settings
BROWSER_TYPE=chrome
HEADLESS_MODE=true

# Server
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── modules/
│   │   │   ├── form_detector.py      # Form detection logic
│   │   │   ├── ai_engine.py          # AI integration
│   │   │   └── data_extractor.py     # Data extraction
│   │   ├── utils/
│   │   │   ├── browser_automation.py # Browser control
│   │   │   └── validators.py         # Data validation
│   │   ├── schemas/
│   │   │   └── schemas.py            # Pydantic models
│   │   ├── routes/
│   │   │   ├── forms.py              # Form endpoints
│   │   │   ├── data_extraction.py    # Extraction endpoints
│   │   │   └── automation.py         # Automation endpoints
│   │   ├── main.py                   # FastAPI app
│   │   └── config.py                 # Configuration
│   ├── requirements.txt
│   ├── .env.example
│   ├── run.sh / run.bat
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── README.md
│
└── README.md
```

## Examples

### Example 1: Detect Forms on a Webpage
```python
import requests

url = "https://example.com/form"
response = requests.get(f"http://localhost:8000/api/forms/detect?url={url}")
forms = response.json()
print(f"Found {len(forms['forms'])} form(s)")
```

### Example 2: Auto-Fill a Form with User Data
```python
import requests

user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123"
}

response = requests.post(
    "http://localhost:8000/api/automation/smart-fill",
    json={
        "url": "https://example.com/form",
        "user_data": user_data
    }
)

result = response.json()
print(f"Filled {result['fields_filled']} fields")
```

## Troubleshooting

### ChromeDriver Issues
- Download the correct version matching your Chrome browser
- Add to PATH: `export PATH=$PATH:/path/to/chromedriver`

### API Key Issues
- Ensure `OPENAI_API_KEY` or `GEMINI_API_KEY` is set in `.env`
- Test keys using the respective API provider's CLI

### Form Not Detected
- Check if the website uses dynamic content (may require headless=false)
- Try increasing timeouts in browser_automation.py

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review API endpoint documentation

## Roadmap

- [ ] Multi-language support
- [ ] Advanced OCR for scanned documents
- [ ] Mobile app support
- [ ] Cloud deployment guides
- [ ] Advanced ML models for field prediction
- [ ] Database integration module
- [ ] Webhook notifications
- [ ] Batch processing
- [ ] UI/UX improvements

---

Built with ❤️ using AI and automation technology
