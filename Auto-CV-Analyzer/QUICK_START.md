# 🚀 Quick Start Guide

## Prerequisites
- ✅ Python 3.11.0 installed
- ✅ pip package manager
- ✅ CVs stored in the dataset directory

## Setup (First Time Only)

### Step 1: Install Dependencies
Double-click `setup.bat` or run:
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your CV Files
Have your CV files ready (PDF or DOCX format). You'll upload them directly in the app.

## Running the Application

### Option 1: Using Batch File (Easiest)
Double-click `run.bat`

### Option 2: Using Command Line
```bash
streamlit run app.py
```

The application will automatically open in your browser at:
**http://localhost:8501**

## Using the Application

### 1️⃣ Job Description Input
- **Option A**: Upload a file (PDF, DOCX, TXT, or JSON)
- **Option B**: Type/paste job description manually

### 2️⃣ Extract Keywords
- Click "🔍 Auto-Extract Keywords" button
- Or manually enter keywords (comma-separated)

### 3️⃣ Configure Settings (Sidebar)
- ✅ Select algorithms (Brute Force, Rabin-Karp, KMP)
- 📁 Verify CV directory path
- 🔠 Toggle case-sensitive matching

### 4️⃣ Start Analysis
- Click "🚀 Start Analysis" button
- Wait for processing to complete

### 5️⃣ View Results
Navigate through tabs:
- **📊 Analysis Results**: Detailed CV rankings and scores
- **📈 Performance Comparison**: Algorithm performance charts
- **💾 Export Data**: Download results as CSV or JSON

## Example Workflow

1. Open the app
2. Upload `example_job_description.json` from `data/job_descriptions/`
3. Click "Auto-Extract Keywords"
4. Click "Start Analysis"
5. View results in the tabs

## Troubleshooting

### App Won't Start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### No CVs Found
- Verify the directory path in the sidebar
- Ensure CVs are in supported formats (PDF, DOCX, TXT, JSON)

### Import Errors
```bash
# Reinstall specific package
pip install streamlit --upgrade
pip install pdfplumber --upgrade
```

## Features to Try

✅ **Multiple Algorithms**: Compare Brute Force, Rabin-Karp, and KMP performance
✅ **Auto-Extraction**: Let the system detect skills automatically
✅ **Filtering**: Filter results by algorithm
✅ **Sorting**: Sort by relevance, time, or comparisons
✅ **Export**: Download results as CSV or JSON
✅ **Visualization**: Interactive charts for performance comparison

## Tips

💡 **For Best Results**:
- Use clear, well-structured job descriptions
- Include specific technical skills and keywords
- Review and edit auto-extracted keywords
- Try different algorithms to compare performance

🎯 **Performance**:
- KMP is usually the fastest
- All algorithms produce the same matches
- Execution time varies with CV size and keyword count

📊 **Data Export**:
- Click "💾 Export Data" tab
- Download as CSV for Excel analysis
- Download as JSON for programmatic access

---

**Need Help?**
Refer to `README.md` for detailed documentation.

**Happy Analyzing! 📄✨**
