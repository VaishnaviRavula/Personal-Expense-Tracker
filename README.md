# SpendWise — Personal Expense Tracker

A responsive personal expense tracker built with Python, Flask, SQLite, HTML, CSS, and Chart.js.

## Features
- Add expenses with title, category, amount, date, and optional notes
- View and delete expense records
- All-time and current-month totals
- Filter by category and month
- Current-month category doughnut chart
- Responsive layout for desktop and mobile
- SQLite database created automatically

## Run locally (Windows)
1. Install Python 3.10 or newer.
2. Open Command Prompt and change directory to this project folder.
3. Create a virtual environment:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bat
   pip install -r requirements.txt
   ```
5. Start the application:
   ```bat
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

## Upload to GitHub
Create an empty GitHub repository, then run these commands inside this folder:
```bat
git init
git add .
git commit -m "Build personal expense tracker with Flask"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Replace the example repository URL with your own.

## Deploy to Render
1. Push the project to GitHub.
2. Sign in to Render and choose **New + → Web Service**.
3. Connect your GitHub repository.
4. Render can use `render.yaml`, or set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Deploy and open the public URL Render provides.

## Important database note
The default SQLite file is local to the application. Many hosting services use an ephemeral filesystem, so data may reset after a restart or redeploy. For persistent production data, configure a persistent disk and set `DATABASE_PATH` to a file on that disk, or use a managed PostgreSQL database and adapt the database layer. Do not store real sensitive financial information in this demonstration project.

## Security note
This is a learning project. Before production use, add authentication, CSRF protection, stronger validation, and a persistent managed database. Set a unique `SECRET_KEY` in deployment settings.
