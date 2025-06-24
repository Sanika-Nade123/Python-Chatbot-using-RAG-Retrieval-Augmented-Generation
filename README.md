# 🧠 PySensei - Your AI-Powered Python Learning Assistant

## 📘 Overview

**PySensei** is an AI-driven educational chatbot that acts as a personalized tutor for Python learners. Built using a combination of Flask, MySQL, FAISS, and Retrieval Augmented Generation (RAG), it delivers **instant, context-aware responses** to Python-related queries—empowering beginners and enthusiasts to learn effectively and independently.

---

## 🎯 Features

- 🔐 **Secure User Authentication** with password hashing and session management  
- 🧑‍🏫 **Role-Based Access Control** (Admins & Users)  
- 💬 **AI-Powered Chat Interface** using FAISS and Sentence Transformers  
- 📚 **Chat History Tracking** and downloadable transcripts  
- 📄 **PDF Report Generation** for user progress  
- 📊 **Admin Dashboard** with user monitoring & analytics  
- 🧠 **Context-Aware Query Handling** using Retrieval Augmented Generation (RAG)

---

## 🧩 Tech Stack

### 💻 Backend
- Python 3.8+
- Flask
- MySQL
- SQLAlchemy ORM
- FAISS (Similarity Search)
- Sentence Transformers
- FPDF2 (for PDF export)
- Werkzeug (for security)

### 🌐 Frontend
- HTML5, CSS3, JavaScript
- Bootstrap (for responsive UI)

---

## 🔒 Security Features

- Hashed Password Storage
- Session Management
- SQL Injection Prevention
- Input Validation
- Role-Based Route Protection

---

## 🔍 Use Cases

- 👩‍🎓 Students and self-learners wanting real-time help with Python
- 🧑‍💻 Developers looking for fast, reliable code explanations
- 🏫 Institutions integrating AI-driven Python tutoring
- 📊 Admins monitoring learning behavior and generating performance insights

---

## 📷 Screenshots

- Login & Registration Screens  
- User Dashboard & Chat History  
- Admin Panel for Monitoring  
- PDF Report Download Feature  

_(Screenshots are available in the repository under the `/screenshots` folder if uploaded)_

---

## 🧪 Test Coverage

All major functionalities were tested, including:

- ✅ User Registration & Login
- ✅ Chatbot Query Accuracy
- ✅ SQL Injection Protection
- ✅ PDF Generation
- ✅ Admin Access Control

---

## 📌 Limitations

- Supports **Python only** (as of now)
- Requires **Internet Connection**
- **No voice input/output** yet
- **Does not execute Python code**

---

## 🚀 Future Scope

- 🔉 Add voice support
- 📱 Launch mobile app version
- 👥 Enable peer-to-peer learning
- 🧪 Embed live code compiler
- 📊 Add advanced admin analytics
- 🌐 Multilingual & Multi-language programming support (Java, C, JavaScript)

---

## 📈 System Requirements

### 💻 Development

- OS: Windows/Linux/macOS
- RAM: Minimum 8GB
- IDE: Visual Studio Code
- Tools: Git, MySQL Workbench, Postman

### 🌐 Browser Compatibility

- Chrome, Firefox, Safari (latest versions)

---

## 🗃️ Database Schema (Simplified)

- `Users`: Stores user details and login credentials
- `Admin`: Stores admin roles and access levels
- `ChatHistory`: Stores user questions and chatbot responses

---

## 📚 References & Acknowledgments

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- FAISS: https://github.com/facebookresearch/faiss
- Python Docs: https://docs.python.org/
- RAG Theory: Facebook AI Research Papers
- Open-source contributions on GitHub

