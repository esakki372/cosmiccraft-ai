# ComicCraft AI

**AI Comic Story Creator powered by Google Gemini and Stable Diffusion.**

A FastAPI-based web application that generates complete comics from text prompts using:
- **Google Gemini Flash** - For quick comic panel outlines
- **Google Gemini Pro** - For rich story narration and dialogue
- **Stable Diffusion** - For AI-generated comic panel images
- **Python FPDF** - For PDF export

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API Key (get one at https://ai.google.dev/)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/esakki372/cosmiccraft-ai.git
cd cosmiccraft-ai
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

4. **Set up environment variables (LOCAL DEVELOPMENT ONLY)**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

5. **Run the app**
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` in your browser.

---

## 🔒 Security - Environment Variables

### ⚠️ CRITICAL: Never commit `.env` file

The `.env` file is **ignored by git** (see `.gitignore`). Always:

**Local Development:**
```bash
cp .env.example .env
# Add your API key to .env
echo "GEMINI_API_KEY=your_real_key_here" > .env
```

**Render Deployment:**
1. Go to Render Dashboard → Your Service → Settings
2. Click "Environment"
3. Add new variable:
   - Key: `GEMINI_API_KEY`
   - Value: `your_actual_api_key`
4. Save and redeploy

**Why this matters:**
- ✅ `.env.example` is safe (has placeholder values)
- ❌ `.env` contains real secrets (must stay private)
- ❌ **Never upload .env to GitHub**
- ✅ Render environment variables are encrypted and secure

---

## 📋 API Endpoints

### Generate Full Comic
```bash
POST /api/generate-comic
Content-Type: application/json

{
    "prompt": "A superhero saves a city from aliens",
    "character": "Captain Amazing",
    "tone": "action-packed"
}
```

**Response:**
```json
{
    "status": "success",
    "outline": "...",
    "story": "...",
    "pdf_path": "/static/exports/comic_abc123.pdf"
}
```

### Generate Outline Only
```bash
POST /api/generate-outline?prompt=Your%20story%20idea
```

### Generate Story Only
```bash
POST /api/generate-story?prompt=outline&character=Hero&tone=adventure
```

### Health Check
```bash
GET /health
```

---

## 📁 Project Structure

```
comiccraft-ai/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── .env.example           # Environment template (SAFE - no secrets)
├── .gitignore             # Prevents .env upload
├── README.md              # This file
├── app/
│   ├── __init__.py
│   ├── routes.py          # API endpoints
│   ├── gemini_flash.py    # Quick outline generation
│   ├── gemini_pro.py      # Story generation
│   ├── image_generator.py # Image generation
│   ├── layout_builder.py  # Comic layout assembly
│   └── exporters.py       # PDF export
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
└── static/
    ├── panels/            # Generated panel images
    └── exports/           # Generated PDFs
```

---

## ⚙️ How It Works

1. **User submits prompt** → `/api/generate-comic`
2. **Gemini Flash** generates a quick outline of 4 panels
3. **Stable Diffusion** generates an image for each panel
4. **Gemini Pro** writes rich dialogue and narration
5. **Layout Builder** combines everything
6. **PDF Exporter** creates a downloadable comic book

---

## 🎨 Features

✅ AI-powered comic generation  
✅ Customizable character and tone  
✅ PDF export  
✅ Responsive web UI  
✅ Render-ready deployment  
✅ CORS enabled for API access  
✅ Secure environment variable handling  

---

## 📦 Deployment on Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your GitHub repo
4. **Add environment variable:**
   - Key: `GEMINI_API_KEY`
   - Value: Your actual API key
5. Deploy!

The app uses `render.yaml` for automatic configuration.

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- **Local**: Create `.env` file and add your key (copy from `.env.example`)
- **Render**: Go to Settings → Environment → Add `GEMINI_API_KEY`
- Make sure the key is not empty!

### Images not generating (showing placeholders)
- This is expected on Render (limited resources)
- Locally, make sure `torch` and `diffusers` are installed
- Use a cloud image API for production: Stability AI, Replicate, or DALL-E

### PDF export fails
- Check `static/exports/` directory exists and is writable
- Ensure all panel images are created successfully
- Check file permissions

### Module import errors
- Run `pip install -r requirements.txt`
- Make sure virtual environment is activated
- Check Python version is 3.9+

---

## 📝 License

MIT

---

## 🤝 Contributing

Found a bug? Have an idea? Open an issue or PR!

---

**Made with ❤️ by ComicCraft AI**
