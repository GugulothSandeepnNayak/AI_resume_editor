# Career-Pilot AI: Complete Running Guide

## 🚀 **Quick Start Commands**

### **Prerequisites Check**
```bash
# Check if Python 3 is installed
python3 --version

# Check if Ollama is installed and running
ollama list

# Check if required models are available
ollama list | grep -E "(llama3|mxbai-embed-large)"
```

### **One-Command Setup & Run**
```bash
# Navigate to project directory
cd /Users/sandeep/Documents/AI_resume_editor

# Activate virtual environment and start backend
source venv/bin/activate && cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📋 **Complete Step-by-Step Guide**

### **Step 1: Prerequisites Setup**

#### **1.1 Install Ollama (if not already installed)**
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

#### **1.2 Pull Required AI Models**
```bash
# Pull the main language model
ollama pull llama3

# Pull the embedding model
ollama pull mxbai-embed-large

# Verify models are available
ollama list
```

**Expected Output:**
```
NAME                SIZE       ID              MODIFIED
llama3              4.7 GB     llama3:latest   2024-01-15 10:30:00
mxbai-embed-large   1.2 GB     mxbai-embed-large:latest 2024-01-15 10:35:00
```

### **Step 2: Python Environment Setup**

#### **2.1 Navigate to Project Directory**
```bash
cd /Users/sandeep/Documents/AI_resume_editor
```

#### **2.2 Activate Virtual Environment**
```bash
source venv/bin/activate
```

**You should see `(venv)` at the beginning of your terminal prompt.**

#### **2.3 Verify Dependencies**
```bash
# Check if all packages are installed
pip list | grep -E "(fastapi|uvicorn|ollama|chromadb|PyPDF2)"
```

**Expected Output:**
```
fastapi                   0.104.1
uvicorn                   0.24.0
ollama                    0.1.7
chromadb                  0.4.18
PyPDF2                    3.0.1
```

### **Step 3: Start the Backend Server**

#### **3.1 Navigate to Backend Directory**
```bash
cd backend
```

#### **3.2 Start FastAPI Server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
Initialized ChromaDB client at ./chroma_db with collection 'resume_collection'
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Keep this terminal window open!** The backend server must stay running.

### **Step 4: Start the Frontend Server**

#### **4.1 Open a New Terminal Window/Tab**

#### **4.2 Navigate to Project Directory**
```bash
cd /Users/sandeep/Documents/AI_resume_editor
```

#### **4.3 Start Frontend Server**
```bash
cd frontend
python3 server.py
```

**Expected Output:**
```
🚀 Frontend server running at http://localhost:3000
📁 Serving files from: /Users/sandeep/Documents/AI_resume_editor/frontend
Press Ctrl+C to stop the server
```

### **Step 5: Access the Application**

#### **5.1 Open Your Web Browser**

#### **5.2 Navigate to the Application**
```
http://localhost:3000
```

#### **5.3 Verify System Status**
- The page should load with a beautiful interface
- Check that the "System Status" shows "Ready" (green)
- If it shows "Not Ready", ensure Ollama is running and models are pulled

---

## 🔧 **Troubleshooting Common Issues**

### **Issue 1: "uvicorn command not found"**
**Solution:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Verify uvicorn is installed
pip show uvicorn

# If not installed, install it
pip install uvicorn
```

### **Issue 2: "Ollama connection failed"**
**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve

# In a new terminal, verify models
ollama list
```

### **Issue 3: "Port 8000 already in use"**
**Solution:**
```bash
# Kill any existing uvicorn processes
pkill -f "uvicorn main:app"

# Wait 2 seconds, then start again
sleep 2
uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Issue 4: "Port 3000 already in use"**
**Solution:**
```bash
# Kill any existing Python server processes
pkill -f "python.*server.py"

# Wait 2 seconds, then start again
sleep 2
python3 server.py
```

### **Issue 5: "Models not found"**
**Solution:**
```bash
# Pull the required models
ollama pull llama3
ollama pull mxbai-embed-large

# Verify they're available
ollama list
```

---

## 📱 **Using the Application**

### **Step 1: Upload Your Resume**
1. Click "Choose File" or drag and drop your resume
2. Supported formats: PDF, TXT, MD
3. Wait for upload confirmation

### **Step 2: Enter Job Description**
1. Paste the job description in the text area
2. Make sure it's detailed and complete
3. Click "Generate Tailored Resume"

### **Step 3: Review Results**
1. View your tailored resume
2. Check the ATS score and breakdown
3. Review recommendations for improvement
4. Copy the optimized resume

---

## 🛑 **Stopping the Application**

### **Method 1: Using Terminal Commands**
```bash
# Stop backend server (in backend terminal)
# Press Ctrl+C

# Stop frontend server (in frontend terminal)
# Press Ctrl+C
```

### **Method 2: Using Process Kill Commands**
```bash
# Kill all application processes
pkill -f "uvicorn main:app"
pkill -f "python.*server.py"

# Verify processes are stopped
ps aux | grep -E "(uvicorn|python.*server)" | grep -v grep
```

---

## 🔄 **Restarting the Application**

### **Quick Restart Commands**
```bash
# Terminal 1 - Backend
cd /Users/sandeep/Documents/AI_resume_editor
source venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd /Users/sandeep/Documents/AI_resume_editor
cd frontend
python3 server.py
```

---

## 📊 **System Requirements**

### **Minimum Requirements**
- **RAM**: 8GB (16GB recommended for smooth operation)
- **Storage**: 10GB free space
- **Python**: 3.8 or higher
- **Internet**: Required for initial model download

### **Recommended Requirements**
- **RAM**: 16GB or more
- **Storage**: 20GB free space
- **CPU**: Multi-core processor
- **GPU**: Not required (CPU-only operation)

---

## 🎯 **Performance Tips**

### **For Faster Processing**
1. **Close unnecessary applications** to free up RAM
2. **Use SSD storage** for faster file operations
3. **Keep models in memory** by using the application regularly
4. **Optimize resume size** (keep under 2MB for faster uploads)

### **For Better Results**
1. **Use detailed job descriptions** with specific requirements
2. **Upload comprehensive resumes** with all relevant experience
3. **Review and iterate** based on ATS score feedback
4. **Keep Ollama running** to avoid model reloading delays

---

## 📞 **Getting Help**

### **If Something Goes Wrong**
1. **Check the terminal output** for error messages
2. **Verify all prerequisites** are installed and running
3. **Restart the application** using the commands above
4. **Check system resources** (RAM, disk space)

### **Common Error Messages**
- **"Connection refused"**: Ollama not running
- **"Model not found"**: Models not pulled
- **"Port in use"**: Another instance running
- **"Permission denied"**: File permission issues

---

## 🎉 **Success Indicators**

### **When Everything is Working**
- ✅ Backend shows "Uvicorn running on http://0.0.0.0:8000"
- ✅ Frontend shows "Frontend server running at http://localhost:3000"
- ✅ Web interface loads without errors
- ✅ System status shows "Ready" (green)
- ✅ Resume upload works
- ✅ Job description processing works
- ✅ ATS scoring generates results

**Congratulations! Your Career-Pilot AI is running successfully! 🚀** 