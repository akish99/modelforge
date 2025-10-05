

 🦠 Plant Disease Detection Web App

A full-stack web application for detecting plant diseases using an AI model. Built with Flask, , and served via a Render deployment.

 🔗 Live Demo

[🌐 Visit the App on Render](https://your-app-url.onrender.com)*

---

📁 Project Structure

```bash
modelforge/
│
├── backend/
│   ├── app.py              # Flask server
│   ├── db.py               # DB logic
│   ├── utils.py            # Helper functions
│   ├── users.db            # SQLite DB
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── Procfile                # Optional Render process file
├── .env                    # API keys (e.g., Gemini)
```

---

 🚀 Features

* 🌱 Upload plant leaf images to detect diseases
* 🔗 Uses Gemini API for inference (optional)
* 🌐 Full frontend with HTML/CSS/JS
* ☁️ Deployable on [Render](https://render.com)

---

🔧 Installation (Local)

1. Clone the repo

```bash
git clone https://github.com/yourusername/plant-disease-detector.git
cd plant-disease-detector
```

2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the app

```bash
python backend/app.py
```

Then go to `http://localhost:10000` in your browser.

---

 🌐 Deployment on Render

 📦 Setup Steps

1. Push code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repo
4. Set:

   * Build Command:(leave blank or use `pip install -r requirements.txt`)
   * Start Command: `python backend/app.py`
   * Environment: Python
   * Port: `10000`
5. Add environment variable (optional):

   ```
   GEMINI_API_KEY=your-google-api-key
   ```

Render will auto-build and deploy the app. You'll get a public URL!

---


 🛠️ Tech Stack

* Backend: Flask, SQLite
* Frontend: HTML5, CSS3, JavaScript
* API: Google Gemini (optional)
* Hosting: Render.com

--


 🙌 Acknowledgments

* Google AI - Gemini API
* Render for free hosting
* Open-source contributors

---

 📄 License

MIT License - feel free to use and modify.

---

