# 📄 Job Description File Format Guide

## 📋 Overview

The Intelligent CV Analyzer supports **4 file formats** for job description upload. Each format has specific requirements for best results.

---

## 1️⃣ TXT Format (`.txt`) - **RECOMMENDED**

### ✅ Required Format
```
Line 1: Job Title
Line 2: Comma-separated skills
```

### 📝 Examples

**Example 1: Graphic Designer**
```
Graphic Designer
Figma, Canva, Adobe Photoshop, Adobe Illustrator, UI/UX Design
```

**Example 2: Data Scientist**
```
Data Scientist
Python, Machine Learning, SQL, Pandas, NumPy, TensorFlow
```

**Example 3: Software Engineer**
```
Software Engineer
Python, JavaScript, React, Node.js, SQL, MongoDB, Git, Docker
```

### ⚠️ Important Notes
- **Line 1** must contain ONLY the job title
- **Line 2** must contain ONLY comma-separated skills
- Skills will be extracted EXACTLY from line 2
- No auto-extraction needed - skills are used directly
- Case-insensitive matching by default

### ✅ Benefits
- ✨ Fastest and most accurate
- ✨ No parsing errors
- ✨ Direct skill extraction
- ✨ Can be reused by uploading

---

## 2️⃣ JSON Format (`.json`)

### ✅ Required Format
```json
{
  "title": "Job Title Here",
  "skills": [
    "Skill 1",
    "Skill 2",
    "Skill 3"
  ]
}
```

### 📝 Example
```json
{
  "title": "Graphic Designer",
  "skills": [
    "Figma",
    "Canva",
    "Adobe Photoshop",
    "Adobe Illustrator",
    "UI/UX Design",
    "Branding",
    "Typography"
  ],
  "saved_at": "2025-10-31T15:30:00"
}
```

### ⚠️ Important Notes
- Must have `"title"` field (string)
- Must have `"skills"` field (array of strings)
- Additional fields (like `saved_at`) are optional
- Skills array is extracted directly

---

## 3️⃣ PDF Format (`.pdf`)

### ⚠️ Usage
- Upload any PDF with job description text
- Text will be extracted automatically
- You MUST use **"Auto-Extract Keywords"** button OR manually enter skills
- Suitable for formal job postings

### 📝 Example Content
```
JOB POSTING

Position: Graphic Designer
Department: Creative

We are looking for a talented Graphic Designer...

Required Skills:
- Figma
- Canva
- Adobe Photoshop
- Adobe Illustrator
```

### 💡 Tip
After uploading PDF, click **"🔍 Auto-Extract Keywords"** to automatically detect skills.

---

## 4️⃣ DOCX/DOC Format (`.docx`, `.doc`)

### ⚠️ Usage
- Upload Word document with job description
- Similar to PDF - text is extracted
- Use **"Auto-Extract Keywords"** OR enter manually

---

## 💾 Save Feature

After entering job description manually, you can **save it for future use**:

### How to Save
1. Enter job description (manual or upload)
2. Extract or enter skills
3. Scroll to **"💾 Save Job Description"** section
4. Enter a job title for the filename
5. Click **"💾 Save as TXT & JSON"**

### What Gets Saved
- **TXT file** (format: Line 1 = title, Line 2 = skills)
- **JSON file** (format: title + skills array)
- Both saved to `data/job_descriptions/` folder
- Can be downloaded directly from the app

### File Naming
Files are saved as: `Job_Title_YYYYMMDD_HHMMSS.txt` / `.json`

**Example:**
- `Graphic_Designer_20251031_153045.txt`
- `Graphic_Designer_20251031_153045.json`

---

## 🎯 Best Practices

### ✅ DO
- Use **TXT format** for fastest, most accurate results
- Keep skills on **one line** (line 2 in TXT)
- Use **comma-separated** format for skills
- Save frequently used job descriptions
- Include exact skill names as they appear in CVs

### ❌ DON'T
- Don't put multiple lines of text in line 2 of TXT files
- Don't forget commas between skills
- Don't include extra spaces before/after skills (they're auto-trimmed)
- Don't use special characters in job titles when saving

---

## 📂 Example Files Included

The app includes these example files in `data/job_descriptions/`:

1. **`Graphic_Designer.txt`** - Graphic Designer position
2. **`example_job_description.txt`** - Software Engineer position  
3. **`example_job_description.json`** - Data Scientist position

You can upload these directly to test the app!

---

## 🔄 Workflow Summary

### Option A: TXT Upload (Fastest)
1. Create TXT file with 2 lines (title, skills)
2. Upload in app
3. Skills automatically extracted ✅
4. Click "Start Analysis"

### Option B: JSON Upload
1. Create or use saved JSON file
2. Upload in app
3. Skills automatically extracted ✅
4. Click "Start Analysis"

### Option C: Manual Entry
1. Type job description in text area
2. Enter skills (comma-separated)
3. Click "💾 Save as TXT & JSON" (optional)
4. Click "Start Analysis"

### Option D: PDF/DOCX Upload
1. Upload file
2. Click "🔍 Auto-Extract Keywords"
3. Review/edit extracted skills
4. Click "💾 Save as TXT & JSON" (optional)
5. Click "Start Analysis"

---

## ❓ FAQ

**Q: What if auto-extract gives wrong results?**  
A: Manually edit the skills in the comma-separated text area. The system will use your manual input.

**Q: Can I save and reuse job descriptions?**  
A: Yes! Use the "💾 Save Job Description" feature after entering skills.

**Q: Which format is best?**  
A: **TXT format** (2 lines) is fastest and most accurate.

**Q: Can I have spaces in skill names?**  
A: Yes! Examples: "Machine Learning", "UI/UX Design", "Problem Solving"

**Q: Case sensitive?**  
A: By default NO. You can enable case-sensitive matching in the sidebar.

---

**💡 Pro Tip:** Create a library of job description TXT files for your common positions. Just 2 lines each - quick to create, easy to reuse! 🚀
