# AI Asset Tagging System

## 📌 Project Overview

The **AI Asset Tagging System** is a Django-based web application that allows users to upload images, provide a text prompt, and automatically detect objects using the **Grounding DINO** AI model. The system displays the detected object names, confidence scores, and bounding box coordinates.

---

## 🚀 Features

* User Registration
* User Login & Logout
* Secure Authentication
* Image Upload
* AI Prompt Input
* Object Detection using Grounding DINO
* Detection Results
* Confidence Score
* Bounding Box Coordinates
* CSV Export
* JSON Export
* Django Admin Panel

---

## 🛠️ Technology Stack

### Backend

* Python 3.x
* Django
* Django REST Framework

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### AI Model

* Grounding DINO
* Hugging Face Transformers
* Pillow (PIL)

### Database

* SQLite (Development)
* MySQL (Optional)

---

## 📂 Project Structure

```
asset_tagging/
│
├── asset_tagging/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── assets/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── serializers.py
│   ├── urls.py
│   ├── services/
│   │   └── grounding_dino.py
│   └── templates/
│
├── media/
│   └── uploads/
│
├── static/
│
├── requirements.txt
└── manage.py
```

---

## 📖 Project Workflow

```
Home Page
      │
      ▼
Register
      │
      ▼
Login
      │
      ▼
Upload Image
      │
      ▼
Enter Prompt
      │
      ▼
Grounding DINO Detection
      │
      ▼
Results
      │
      ├── Detected Tag
      ├── Confidence Score
      └── Bounding Box
```

---

## 👤 User Module

* Register Account
* Login
* Upload Images
* Enter Detection Prompt
* View Detection Results
* Export Results
* Logout

---

## 🔐 Admin Module

The Django Admin Panel provides project management features:

* View Registered Users
* Manage Uploaded Images
* View Detection Results
* Manage Datasets
* Delete Images
* Activate/Deactivate Users

Admin URL:

```
/admin/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/asset-tagging.git
```

### Move into Project

```bash
cd asset-tagging
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 📊 Detection Output

Each detection includes:

* Uploaded Image
* Detected Object Name
* Confidence Score
* Bounding Box Coordinates

---

## 📤 Export

The application supports:

* CSV Export
* JSON Export

---

## 📌 Future Improvements

* Bulk Image Upload
* Batch AI Detection
* User Profile Management
* Detection History
* Image Search
* Docker Deployment
* Cloud Storage Integration
* JWT Authentication
* REST API

---

## 👨‍💻 Developer

**Hariharan M**

Python Full Stack Developer

---

## 📄 License

This project is developed for educational and portfolio purposes.
