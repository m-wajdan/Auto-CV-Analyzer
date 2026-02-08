# Auto-CV-Analyzer
Design and Analysis of Algorithm's final project, A CV analyzer that tells the relativity score of a CV by detecting the keywords provided by the recruiter. 
# 📄 Intelligent CV Analyzer

A Streamlit-based web application that automatically analyzes resumes (CVs) using three classical string matching algorithms: **Brute Force**, **Rabin-Karp**, and **KMP (Knuth-Morris-Pratt)**. The system extracts text from CVs, matches required skills from job descriptions, computes relevance scores, and provides comprehensive algorithm performance comparisons.

## 🎯 Project Overview

**Title:** Design and Implementation of a CV Analyzer using String Matching Algorithms for Automated Skill Extraction and Job Fit Evaluation

**Purpose:** Automate CV screening by extracting skills from resumes and comparing them against job requirements using classical string matching algorithms.

## ✨ Features

### Core Functionality
- ✅ **Multiple File Format Support**: PDF, DOCX, TXT, and JSON
- ✅ **Dual Input Mode**: Upload job description files or enter manually
- ✅ **Three String Matching Algorithms**: Brute Force, Rabin-Karp, and KMP
- ✅ **Automatic CV Processing**: Batch process all CVs from a directory
- ✅ **Relevance Score Calculation**: (Matched Keywords / Total Keywords) × 100
- ✅ **Performance Metrics**: Execution time and comparison counts
- ✅ **Case-Sensitive Matching**: Optional toggle for precise matching

### User Interface
- 📊 **Interactive Dashboard**: Modern Streamlit interface with tabs
- 📈 **Performance Comparison Charts**: Visual algorithm analysis
- 🏆 **CV Ranking**: Automatic ranking by relevance score
- 💾 **Data Export**: CSV and JSON export options
- 🎨 **Professional Design**: Clean, intuitive UI with custom styling

### Algorithm Features
- **Brute Force**: Simple character-by-character comparison
- **Rabin-Karp**: Efficient hash-based pattern matching
- **KMP**: Optimized matching with prefix function

## 📁 Project Structure

```
intelligent-cv-analyzer/
│
├── app.py                          # Main Streamlit application
│
├── algorithms/
│   ├── __init__.py
│   ├── brute_force.py              # Brute Force implementation
│   ├── rabin_karp.py               # Rabin-Karp implementation
│   └── kmp.py                      # KMP implementation
│
├── utils/
│   ├── __init__.py
│   ├── file_reader.py              # Text extraction from PDF/DOCX/TXT/JSON
│   ├── text_cleaner.py             # Text preprocessing and keyword extraction
│   └── performance_metrics.py      # Performance tracking and comparison
│
├── data/
│   ├── cvs/                        # CV storage 
│   └── job_descriptions/           # Job description storage
│
├── results/
│   ├── analysis_results.csv        # Exported analysis results
│   └── performance_summary.json    # Algorithm performance data
│
├── charts/                         # Saved charts (if needed)
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11.0
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "D:\Uni Material\Sem 5\Design and Analysis of Algorithms\Assignment 2 StreamLit"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Configure Algorithms
In the sidebar:
- ✅ Select which algorithms to use (Brute Force, Rabin-Karp, KMP)
- 🔠 Toggle case-sensitive matching if needed

### 2. Enter Job Description
**Option A: Upload File**
- Click "Choose a file" and upload a PDF, DOCX, TXT, or JSON file
- The system will automatically extract text

**Option B: Manual Input**
- Type or paste the job description in the text area

### 3. Define Required Skills
- Click "🔍 Auto-Extract Keywords" to automatically detect skills
- Or manually enter comma-separated keywords
- Review and edit the keyword list as needed

### 4. Upload CV Files
- Click "Choose CV files" and select one or multiple PDF/DOCX files
- You can upload as many CVs as you want
- View the list of selected files

### 5. Start Analysis
- Click "🚀 Start Analysis" button
- Wait for text extraction and processing to complete
- Progress bars show current status

### 6. View Results
Navigate through tabs:

**📊 Analysis Results**
- Summary metrics (CVs analyzed, average score, processing time)
- Detailed results table (filterable and sortable)
- Top 10 matching CVs with rankings

**📈 Performance Comparison**
- Algorithm performance metrics
- Execution time comparison charts
- Character comparison analysis
- Key insights and recommendations

**💾 Export Data**
- Download results as CSV or JSON
- Save to results folder
- Preview data before export

## 🧮 Algorithm Details

### Brute Force Algorithm
**Approach:** Simple character-by-character pattern matching
**Time Complexity:** O(n×m) where n = text length, m = pattern length
**Use Case:** Baseline for comparison, works on all inputs

### Rabin-Karp Algorithm
**Approach:** Rolling hash function for efficient substring search
**Time Complexity:** O(n+m) average case, O(n×m) worst case
**Use Case:** Good for multiple pattern searching with hash optimization

### KMP Algorithm
**Approach:** Prefix function to avoid unnecessary comparisons
**Time Complexity:** O(n+m)
**Use Case:** Most efficient for single pattern searching

## 📊 Performance Metrics

For each algorithm, the system tracks:
- **Execution Time**: Milliseconds taken for analysis
- **Character Comparisons**: Total number of character comparisons
- **Relevance Score**: Percentage of matched keywords
- **Efficiency**: Comparisons per character ratio

## 📝 Example Output

### Analysis Results Table
| CV File | Algorithm | Matches | Total Keywords | Relevance Score (%) | Execution Time (ms) | Comparisons |
|---------|-----------|---------|----------------|---------------------|---------------------|
| CV1.pdf | Brute Force | 8 | 10 | 80.0 | 152.3 | 20312 |
| CV1.pdf | Rabin-Karp  | 8 | 10 | 80.0 | 96.1 | 10322  |
| CV1.pdf | KMP         | 8 | 10 | 80.0 | 72.5 | 8210   |

### Performance Summary
```json
{
  "fastest_algorithm": "KMP",
  "fastest_time": 72.5,
  "most_efficient_algorithm": "KMP",
  "most_efficient_comparisons": 8210,
  "highest_score_algorithm": "KMP",
  "highest_score_value": 80.0
}
```

## 🗂️ Supported File Formats

### Input Formats
- **PDF**: `.pdf` files (using pdfplumber)
- **Word**: `.docx`, `.doc` files (using docx2txt)
- **Text**: `.txt` files (plain text)
- **JSON**: `.json` files (structured data)

### Output Formats
- **CSV**: Tabular data export
- **JSON**: Structured data export

## ⚙️ Configuration Options

### Sidebar Settings
- **Algorithm Selection**: Choose which algorithms to run
- **CV Directory Path**: Specify where CVs are stored
- **Case Sensitivity**: Toggle case-sensitive matching

### Keyword Extraction
- **Auto-Extract**: Automatically detect skills from job description
- **Manual Entry**: Enter comma-separated keywords
- **Normalization**: Automatic deduplication and cleaning

## 🐛 Troubleshooting

### Common Issues

**1. Directory Not Found**
- Verify the CV dataset path in the sidebar
- Ensure the directory exists and contains CV files

**2. No CVs Loaded**
- Check that CVs are in supported formats (PDF, DOCX, TXT, JSON)
- Verify files are not corrupted

**3. Module Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**4. Streamlit Won't Start**
```bash
# Check Python version
python --version  # Should be 3.11.0

# Reinstall Streamlit
pip install streamlit --upgrade
```

## 📊 Dataset Information

**Default Dataset Path:**
```
D:\Uni Material\Sem 5\Design and Analysis of Algorithms\Assignment 2\DataSet\DataSet
```

The application automatically loads all supported CV files from this directory.

## 🔬 Technical Details

### Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **pdfplumber**: PDF text extraction
- **docx2txt**: DOCX text extraction

### Python Version
- **Required**: Python 3.11.0
- **Tested**: Python 3.11.0

## 📄 License

This project is created for educational purposes as part of the Design and Analysis of Algorithms course.

## 👥 Author

Created as part of **Assignment 2** - Design and Analysis of Algorithms (Semester 5)

## 🙏 Acknowledgments

- Classical string matching algorithms: Brute Force, Rabin-Karp, KMP
- Streamlit framework for rapid web app development
- Open-source libraries for file processing

---

**For support or questions, please refer to the course materials or instructor.**

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Access the app
# Open browser to http://localhost:8501
```

**Happy CV Analyzing! 📄✨**
