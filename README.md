📅 Deadline Tracker — AI-Powered Academic Planner

An AI-powered academic deadline management application built with Python and Streamlit. It helps students organize academic tasks, extract deadlines from uploaded images, monitor progress, and receive email reminders so they can stay on track.

✨ Features

- **AI-Powered Deadline Extraction:** Upload academic images and use Gemini Vision AI to extract deadline information.
- **Interactive Dashboard:** View total tasks, completed tasks, pending tasks, and overdue tasks.
- **Task Management:** Track deadlines and mark tasks as completed.
- **Search and Filters:** Find tasks using search, status filters, and sorting options.
- **Upcoming Deadlines:** View important tasks and upcoming due dates.
- **Email Notifications:** Send deadline digest emails manually.
- **Automated Daily Reminders:** Schedule daily email digests using Windows Task Scheduler.
- **SQLite Database:** Store task information locally.
- **Custom User Interface:** A styled Streamlit interface for easier task management.

🛠️ Technologies Used

- **Python** — Application logic
- **Streamlit** — Web application interface
- **Google Gemini Vision AI** — Image-based deadline extraction
- **SQLite** — Local database
- **Python Email Libraries / SMTP** — Email notifications
- **Windows Task Scheduler** — Automated daily reminders
- **python-dotenv** — Environment variable management

 📁 Project Structure

```text
DeadlineTracker/
├── app.py
├── prompts.py
├── gemini_service.py
├── database.py
├── email_service.py
├── send_daily_digest.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: `requirements.txt` should be created if it does not already exist. The `.env` file contains private configuration and should not be uploaded to GitHub.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ushacmshetty/Deadline-Tracker.git
cd Deadline-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit python-dotenv
```

Install any additional packages required by the project, including the Gemini SDK and email-related dependencies.

### 4. Configure environment variables

Create a `.env` file in the project root and add the configuration variables required by your code.

Example placeholders:

```env
GEMINI_API_KEY=your_gemini_api_key
SMTP_EMAIL=your_email_address
SMTP_PASSWORD=your_email_app_password
```

Use the exact variable names expected by your Python files. Never publish real API keys, email passwords, or other secrets.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📧 Automated Email Reminders

The project includes a script for sending a daily deadline digest:

```bash
python send_daily_digest.py
```

On Windows, this script can be configured in **Task Scheduler** to run daily at a chosen time. Automatic delivery depends on the computer being available, an internet connection, and valid email configuration.

## 🎯 Project Objective

The objective of Deadline Tracker is to help students manage academic responsibilities more efficiently by combining AI-based deadline extraction, task tracking, and email reminders in one application.

## 🚀 Future Enhancements

- Calendar integration
- Push notifications
- User authentication
- Export tasks to CSV or PDF
- Cloud database support
- More advanced AI-based task prioritization

## 👩‍💻 Author

**Usha C M**

BCA Graduate | Aspiring Software Developer

GitHub: [@ushacmshetty](https://github.com/ushacmshetty)

## ⭐ Support

If you find this project useful, consider giving the repository a star on GitHub!
