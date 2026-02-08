"""
Intelligent CV Analyzer - Streamlit Web Application
Analyzes CVs using Brute Force, Rabin-Karp, and KMP string matching algorithms.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Import custom modules
from algorithms import brute_force, rabin_karp, kmp
from utils import file_reader, text_cleaner, performance_metrics

# Page configuration
st.set_page_config(
    page_title="Intelligent CV Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Dataset directory path
DEFAULT_CV_DIRECTORY = r"D:\Uni Material\Sem 5\Design and Analysis of Algorithms\Assignment 2\DataSet\DataSet"


def main():
    # Header
    st.markdown('<h1 class="main-header">📄 Intelligent CV Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Automated CV Screening using Classical String Matching Algorithms</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/resume.png", width=100)
        st.title("⚙️ Configuration")
        
        # Algorithm selection
        st.subheader("🔍 Select Algorithms")
        use_brute_force = st.checkbox("Brute Force", value=True)
        use_rabin_karp = st.checkbox("Rabin-Karp", value=True)
        use_kmp = st.checkbox("KMP", value=True)
        
        algorithms_selected = []
        if use_brute_force:
            algorithms_selected.append(('Brute Force', brute_force))
        if use_rabin_karp:
            algorithms_selected.append(('Rabin-Karp', rabin_karp))
        if use_kmp:
            algorithms_selected.append(('KMP', kmp))
        
        st.divider()
        
        # Case sensitivity
        case_sensitive = st.checkbox("Case Sensitive Matching", value=False)
        
        st.divider()
        
        # About
        with st.expander("ℹ️ About"):
            st.write("""
            **Intelligent CV Analyzer**
            
            This application uses three classical string matching algorithms to analyze CVs:
            - **Brute Force**: Simple pattern matching
            - **Rabin-Karp**: Hash-based matching
            - **KMP**: Efficient pattern matching with prefix function
            
            **How to use:**
            1. Upload or enter a job description
            2. Extract or enter required skills/keywords
            3. Upload CV files (PDF or DOCX)
            4. Click "Start Analysis" to begin
            """)
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Job Description", "📊 Analysis Results", "📋 Analysis Summary", "📈 Performance Comparison", "💾 Export Data"])
    
    # Tab 1: Job Description Input
    with tab1:
        st.header("1️⃣ Job Description Input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Upload Job Description File")
            uploaded_file = st.file_uploader(
                "Choose a file (PDF, DOCX, TXT, JSON)",
                type=['pdf', 'docx', 'doc', 'txt', 'json'],
                key="job_file"
            )
            
            if uploaded_file:
                file_content = uploaded_file.read()
                
                # Special handling for TXT files (expected format: line 1 = title, line 2 = skills)
                if uploaded_file.name.lower().endswith('.txt'):
                    text = file_reader.extract_text_from_txt(file_content=file_content)
                    job_title, skills = file_reader.parse_job_description_txt(text)
                    
                    if job_title:
                        st.session_state['job_title'] = job_title
                        st.success(f"✅ Job Title: {job_title}")
                    
                    if skills:
                        st.session_state['keywords'] = skills
                        st.session_state['job_text'] = text
                        st.success(f"✅ Extracted {len(skills)} skills from file")
                    else:
                        st.warning("⚠️ No skills found on line 2. Please check format.")
                    
                    with st.expander("📄 View File Content"):
                        st.text(text)
                elif uploaded_file.name.lower().endswith('.json'):
                    # Parse JSON format
                    try:
                        text = file_content.decode('utf-8')
                        data = json.loads(text)
                        
                        if 'title' in data:
                            st.session_state['job_title'] = data['title']
                            st.success(f"✅ Job Title: {data['title']}")
                        
                        if 'skills' in data and isinstance(data['skills'], list):
                            st.session_state['keywords'] = data['skills']
                            st.session_state['job_text'] = text
                            st.success(f"✅ Extracted {len(data['skills'])} skills from JSON")
                        else:
                            st.warning("⚠️ 'skills' array not found in JSON.")
                        
                        with st.expander("📄 View JSON Content"):
                            st.json(data)
                    except json.JSONDecodeError:
                        st.error("❌ Invalid JSON format")
                    except Exception as e:
                        st.error(f"❌ Error parsing JSON: {str(e)}")
                else:
                    # For PDF, DOCX - extract full text
                    job_text = file_reader.read_file(file_content=file_content, filename=uploaded_file.name)
                    st.session_state['job_text'] = job_text
                    
                    with st.expander("📄 View Extracted Text"):
                        st.text_area("Job Description", job_text, height=200, key="extracted_job_text")
        
        with col2:
            st.subheader("Or Enter Manually")
            manual_job_text = st.text_area(
                "Job Description",
                height=200,
                placeholder="Enter job description here...",
                key="manual_job_input"
            )
            
            if manual_job_text:
                st.session_state['job_text'] = manual_job_text
        
        st.divider()
        
        # Keywords extraction
        st.subheader("🎯 Required Skills/Keywords")
        
        col3, col4 = st.columns([3, 1])
        
        with col3:
            if 'job_text' in st.session_state and st.session_state['job_text']:
                # Auto-extract keywords
                if st.button("🔍 Auto-Extract Keywords", type="secondary"):
                    extracted_keywords = text_cleaner.extract_skills_from_job_description(st.session_state['job_text'])
                    st.session_state['keywords'] = extracted_keywords
                    st.success(f"Extracted {len(extracted_keywords)} keywords!")
                
                # Manual keyword input
                keywords_input = st.text_area(
                    "Enter keywords (comma-separated)",
                    value=', '.join(st.session_state.get('keywords', [])) if 'keywords' in st.session_state else '',
                    height=100,
                    placeholder="Python, Machine Learning, SQL, etc."
                )
                
                if keywords_input:
                    keywords_list = text_cleaner.extract_keywords(keywords_input)
                    keywords_list = text_cleaner.normalize_keywords(keywords_list)
                    st.session_state['keywords'] = keywords_list
            else:
                st.warning("⚠️ Please enter or upload a job description first.")
                keywords_input = st.text_area(
                    "Enter keywords (comma-separated)",
                    height=100,
                    placeholder="Python, Machine Learning, SQL, etc."
                )
                
                if keywords_input:
                    keywords_list = text_cleaner.extract_keywords(keywords_input)
                    keywords_list = text_cleaner.normalize_keywords(keywords_list)
                    st.session_state['keywords'] = keywords_list
        
        with col4:
            if 'keywords' in st.session_state and st.session_state['keywords']:
                st.metric("Total Keywords", len(st.session_state['keywords']))
                with st.expander("View Keywords"):
                    for i, kw in enumerate(st.session_state['keywords'], 1):
                        st.write(f"{i}. {kw}")
        
        # Save Job Description Feature
        if 'keywords' in st.session_state and st.session_state['keywords']:
            st.divider()
            st.subheader("💾 Save Job Description")
            
            col_save1, col_save2 = st.columns(2)
            
            with col_save1:
                job_title_save = st.text_input(
                    "Job Title (for filename)",
                    value=st.session_state.get('job_title', 'Job_Description'),
                    key="save_job_title"
                )
            
            with col_save2:
                st.write("")
                st.write("")
                if st.button("💾 Save as TXT & JSON", use_container_width=True):
                    try:
                        # Sanitize filename
                        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in job_title_save)
                        safe_filename = safe_filename.replace(' ', '_')
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        
                        # Save as TXT (Line 1: Title, Line 2: Skills)
                        txt_filename = f"data/job_descriptions/{safe_filename}_{timestamp}.txt"
                        txt_content = f"{job_title_save}\n{', '.join(st.session_state['keywords'])}"
                        
                        with open(txt_filename, 'w', encoding='utf-8') as f:
                            f.write(txt_content)
                        
                        # Save as JSON
                        json_filename = f"data/job_descriptions/{safe_filename}_{timestamp}.json"
                        json_content = {
                            "title": job_title_save,
                            "skills": st.session_state['keywords'],
                            "saved_at": datetime.now().isoformat()
                        }
                        
                        with open(json_filename, 'w', encoding='utf-8') as f:
                            json.dump(json_content, f, indent=2)
                        
                        st.success(f"✅ Saved successfully!")
                        st.info(f"📁 **TXT:** `{txt_filename}`")
                        st.info(f"📁 **JSON:** `{json_filename}`")
                        
                        # Provide download buttons
                        col_dl1, col_dl2 = st.columns(2)
                        
                        with col_dl1:
                            st.download_button(
                                label="⬇️ Download TXT",
                                data=txt_content,
                                file_name=f"{safe_filename}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        
                        with col_dl2:
                            st.download_button(
                                label="⬇️ Download JSON",
                                data=json.dumps(json_content, indent=2),
                                file_name=f"{safe_filename}.json",
                                mime="application/json",
                                use_container_width=True
                            )
                    
                    except Exception as e:
                        st.error(f"❌ Error saving files: {str(e)}")
        
        st.divider()
        
        # CV Upload Section
        st.subheader("📄 Upload CV Files")
        uploaded_cvs = st.file_uploader(
            "Choose CV files (PDF or DOCX)",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            key="cv_files",
            help="You can upload multiple CV files at once"
        )
        
        if uploaded_cvs:
            st.info(f"📁 {len(uploaded_cvs)} CV file(s) selected")
            with st.expander("View selected files"):
                for i, file in enumerate(uploaded_cvs, 1):
                    st.write(f"{i}. {file.name} ({file.size / 1024:.2f} KB)")
        
        st.divider()
        
        # Start Analysis Button
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            if 'keywords' not in st.session_state or not st.session_state['keywords']:
                st.error("❌ Please enter keywords before starting analysis!")
            elif not algorithms_selected:
                st.error("❌ Please select at least one algorithm!")
            elif not uploaded_cvs:
                st.error("❌ Please upload at least one CV file!")
            else:
                with st.spinner("🔄 Analyzing CVs... This may take a moment."):
                    # Extract text from uploaded CVs
                    cvs = {}
                    extraction_progress = st.progress(0)
                    extraction_status = st.empty()
                    
                    for i, uploaded_file in enumerate(uploaded_cvs):
                        extraction_status.text(f"Extracting text from {uploaded_file.name}...")
                        
                        try:
                            file_content = uploaded_file.read()
                            cv_text = file_reader.read_file(file_content=file_content, filename=uploaded_file.name)
                            
                            if cv_text and not cv_text.startswith("Error"):
                                cvs[uploaded_file.name] = cv_text
                            else:
                                st.warning(f"⚠️ Could not extract text from {uploaded_file.name}")
                        except Exception as e:
                            st.warning(f"⚠️ Error processing {uploaded_file.name}: {str(e)}")
                        
                        extraction_progress.progress((i + 1) / len(uploaded_cvs))
                    
                    extraction_progress.empty()
                    extraction_status.empty()
                    
                    if not cvs:
                        st.error("❌ No valid text could be extracted from the uploaded CVs!")
                    else:
                        st.success(f"✅ Successfully extracted text from {len(cvs)} CV(s)")
                        
                        # Analyze each CV with selected algorithms
                        cv_results = {}
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        total_operations = len(cvs) * len(algorithms_selected)
                        current_operation = 0
                        
                        for cv_file, cv_text in cvs.items():
                            cv_results[cv_file] = []
                            
                            for algo_name, algo_module in algorithms_selected:
                                status_text.text(f"Analyzing {cv_file} with {algo_name}...")
                                
                                result = algo_module.analyze_text(
                                    cv_text,
                                    st.session_state['keywords'],
                                    case_sensitive=case_sensitive
                                )
                                
                                cv_results[cv_file].append(result)
                                
                                current_operation += 1
                                progress_bar.progress(current_operation / total_operations)
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Store results in session state
                        st.session_state['cv_results'] = cv_results
                        st.session_state['analysis_complete'] = True
                        
                        st.success("✅ Analysis Complete!")
                        st.balloons()
    
    # Tab 2: Analysis Results
    with tab2:
        st.header("📊 Analysis Results")
        
        if 'analysis_complete' in st.session_state and st.session_state['analysis_complete']:
            cv_results = st.session_state['cv_results']
            
            # Aggregate results
            df_results = performance_metrics.aggregate_results(cv_results)
            
            # Display summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total CVs Analyzed", len(cv_results))
            
            with col2:
                avg_score = df_results['Relevance Score (%)'].mean()
                st.metric("Average Relevance Score", f"{avg_score:.2f}%")
            
            with col3:
                total_time = df_results['Execution Time (ms)'].sum()
                st.metric("Total Processing Time", f"{total_time:.2f} ms")
            
            with col4:
                best_cv = df_results.loc[df_results['Relevance Score (%)'].idxmax(), 'CV File']
                st.metric("Best Matching CV", best_cv[:20] + "..." if len(best_cv) > 20 else best_cv)
            
            st.divider()
            
            # Filter options
            col1, col2 = st.columns([1, 3])
            
            with col1:
                filter_algorithm = st.selectbox(
                    "Filter by Algorithm",
                    ['All'] + [algo[0] for algo in algorithms_selected]
                )
            
            with col2:
                sort_by = st.selectbox(
                    "Sort by",
                    ['Relevance Score (%)', 'Execution Time (ms)', 'Comparisons', 'CV File']
                )
            
            # Prepare dataframe for display and compute ordering of CV sections
            df_display = df_results.copy()
            
            if filter_algorithm != 'All':
                df_display = df_display[df_display['Algorithm'] == filter_algorithm]
            
            # Determine CV ordering based on selected sort option
            if sort_by == 'CV File':
                cv_order = sorted(df_display['CV File'].unique())
            else:
                # Aggregate metric per CV (mean) to drive sorting of expanders
                cv_metric = (
                    df_display.groupby('CV File', as_index=True)[sort_by]
                    .mean()
                    .sort_values(ascending=False if sort_by == 'Relevance Score (%)' else True)
                )
                cv_order = cv_metric.index.tolist()
            
            # Display results table - Grouped by CV
            st.subheader("📋 Detailed Results by CV")
            
            # Group results by CV file in the computed order
            for cv_file in cv_order:
                with st.expander(f"📄 {cv_file}", expanded=False):
                    cv_data = df_display[df_display['CV File'] == cv_file]
                    
                    if not cv_data.empty:
                        # Get matched and missing keywords (same for all algorithms)
                        matched = cv_data.iloc[0]['Matched Keywords']
                        missing = cv_data.iloc[0]['Missing Keywords']
                        
                        # Display keywords
                        col_match, col_miss = st.columns(2)
                        with col_match:
                            st.markdown("**✅ Matched Keywords:**")
                            if matched:
                                st.success(matched)
                            else:
                                st.info("None")
                        
                        with col_miss:
                            st.markdown("**❌ Missing Keywords:**")
                            if missing:
                                st.error(missing)
                            else:
                                st.info("None")
                        
                        st.divider()
                        
                        # Algorithm comparison for this CV
                        algo_data = cv_data[['Algorithm', 'Matches', 'Relevance Score (%)', 'Execution Time (ms)', 'Comparisons']].copy()
                        
                        st.markdown("**Algorithm Performance:**")
                        st.dataframe(
                            algo_data,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Relevance Score (%)": st.column_config.ProgressColumn(
                                    "Relevance (%)",
                                    format="%.2f%%",
                                    min_value=0,
                                    max_value=100,
                                )
                            }
                        )
            
            st.divider()
            
            # Top CVs ranking
            st.subheader("🏆 Top Matching CVs")
            
            rankings = performance_metrics.rank_cvs_by_relevance(cv_results)
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.write("**Top 10 CVs by Relevance:**")
                for i, (cv_file, score) in enumerate(rankings[:10], 1):
                    st.write(f"**{i}.** {cv_file} - {score:.2f}%")
            
            with col2:
                # Create bar chart for top CVs
                top_10_df = pd.DataFrame(rankings[:10], columns=['CV', 'Score'])
                fig = px.bar(
                    top_10_df,
                    x='Score',
                    y='CV',
                    orientation='h',
                    title='Top 10 CVs by Relevance Score',
                    labels={'Score': 'Relevance Score (%)', 'CV': 'CV File'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("👈 Please complete the job description and start analysis in the first tab.")
    
    # Tab 3: Analysis Summary
    with tab3:
        st.header("📋 Analysis Summary")
        
        if 'analysis_complete' in st.session_state and st.session_state['analysis_complete']:
            cv_results = st.session_state['cv_results']
            df_results = performance_metrics.aggregate_results(cv_results)
            
            st.markdown("### 📊 Quick Overview of All CVs")
            st.markdown("*At-a-glance summary of each candidate's profile with key metrics*")
            
            st.divider()
            
            # Group by CV and create summary cards
            cv_summaries = []
            for cv_file in sorted(cv_results.keys()):
                cv_data = df_results[df_results['CV File'] == cv_file]
                
                if not cv_data.empty:
                    # Get average metrics across all algorithms for this CV
                    avg_relevance = cv_data['Relevance Score (%)'].mean()
                    avg_exec_time = cv_data['Execution Time (ms)'].mean()
                    total_keywords = len(st.session_state['keywords'])
                    matches = cv_data.iloc[0]['Matches']
                    matched_keywords = cv_data.iloc[0]['Matched Keywords']
                    missing_keywords = cv_data.iloc[0]['Missing Keywords']
                    
                    cv_summaries.append({
                        'cv_file': cv_file,
                        'avg_relevance': avg_relevance,
                        'avg_exec_time': avg_exec_time,
                        'matches': matches,
                        'total_keywords': total_keywords,
                        'matched_keywords': matched_keywords,
                        'missing_keywords': missing_keywords
                    })
            
            # Sort by relevance score (descending)
            cv_summaries.sort(key=lambda x: x['avg_relevance'], reverse=True)
            
            # Display summary cards in a grid
            for idx, summary in enumerate(cv_summaries, 1):
                # Determine color based on relevance score
                if summary['avg_relevance'] >= 70:
                    border_color = "#28a745"  # Green
                    badge = "🟢 Excellent Match"
                elif summary['avg_relevance'] >= 50:
                    border_color = "#ffc107"  # Yellow
                    badge = "🟡 Good Match"
                elif summary['avg_relevance'] >= 30:
                    border_color = "#fd7e14"  # Orange
                    badge = "🟠 Fair Match"
                else:
                    border_color = "#dc3545"  # Red
                    badge = "🔴 Poor Match"
                
                # Create card with custom styling
                st.markdown(f"""
                <div style="
                    border: 3px solid {border_color};
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background: linear-gradient(135deg, rgba(30, 136, 229, 0.05) 0%, rgba(30, 136, 229, 0.02) 100%);
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0; color: #1E88E5;">#{idx} 📄 {summary['cv_file']}</h3>
                        <span style="
                            background-color: {border_color};
                            color: white;
                            padding: 5px 15px;
                            border-radius: 20px;
                            font-weight: bold;
                            font-size: 0.9rem;
                        ">{badge}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "📊 Relevance Score",
                        f"{summary['avg_relevance']:.2f}%",
                        delta=f"{summary['avg_relevance'] - 50:.2f}%" if summary['avg_relevance'] != 50 else None
                    )
                
                with col2:
                    st.metric(
                        "✅ Skills Matched",
                        f"{summary['matches']}/{summary['total_keywords']}",
                        delta=f"{(summary['matches']/summary['total_keywords']*100):.0f}% coverage"
                    )
                
                with col3:
                    st.metric(
                        "⚡ Avg Processing Time",
                        f"{summary['avg_exec_time']:.3f} ms"
                    )
                
                with col4:
                    missing_count = summary['total_keywords'] - summary['matches']
                    st.metric(
                        "❌ Skills Missing",
                        missing_count,
                        delta=f"-{missing_count}" if missing_count > 0 else "Perfect!",
                        delta_color="inverse"
                    )
                
                # Skills breakdown in expander
                with st.expander("🔍 View Skill Details", expanded=False):
                    col_skills1, col_skills2 = st.columns(2)
                    
                    with col_skills1:
                        st.markdown("**✅ Matched Skills:**")
                        if summary['matched_keywords']:
                            matched_list = summary['matched_keywords'].split(', ')
                            for skill in matched_list:
                                st.markdown(f"- ✓ {skill}")
                        else:
                            st.info("No skills matched")
                    
                    with col_skills2:
                        st.markdown("**❌ Missing Skills:**")
                        if summary['missing_keywords']:
                            missing_list = summary['missing_keywords'].split(', ')
                            for skill in missing_list:
                                st.markdown(f"- ✗ {skill}")
                        else:
                            st.success("All skills present!")
                
                st.markdown("---")
            
            # Summary statistics at the bottom
            st.divider()
            st.subheader("📈 Overall Statistics")
            
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("Total CVs Analyzed", len(cv_summaries))
            
            with col_stat2:
                avg_all = sum(s['avg_relevance'] for s in cv_summaries) / len(cv_summaries)
                st.metric("Average Relevance", f"{avg_all:.2f}%")
            
            with col_stat3:
                excellent = sum(1 for s in cv_summaries if s['avg_relevance'] >= 70)
                st.metric("Excellent Matches (≥70%)", excellent)
            
            with col_stat4:
                poor = sum(1 for s in cv_summaries if s['avg_relevance'] < 30)
                st.metric("Poor Matches (<30%)", poor)
            
        else:
            st.info("👈 Please complete the job description and start analysis in the first tab.")
    
    # Tab 4: Performance Comparison
    with tab4:
        st.header("📈 Algorithm Performance Comparison")
        
        if 'analysis_complete' in st.session_state and st.session_state['analysis_complete']:
            cv_results = st.session_state['cv_results']
            
            # Calculate average metrics across all CVs for each algorithm
            algo_metrics = {}
            
            for cv_file, results in cv_results.items():
                for result in results:
                    algo_name = result['algorithm']
                    if algo_name not in algo_metrics:
                        algo_metrics[algo_name] = {
                            'execution_times': [],
                            'comparisons': [],
                            'relevance_scores': []
                        }
                    
                    algo_metrics[algo_name]['execution_times'].append(result['execution_time'])
                    algo_metrics[algo_name]['comparisons'].append(result['comparisons'])
                    algo_metrics[algo_name]['relevance_scores'].append(result['relevance_score'])
            
            # Calculate averages
            algo_comparison = []
            for algo_name, metrics in algo_metrics.items():
                algo_comparison.append({
                    'Algorithm': algo_name,
                    'Avg Execution Time (ms)': sum(metrics['execution_times']) / len(metrics['execution_times']),
                    'Avg Comparisons': sum(metrics['comparisons']) / len(metrics['comparisons']),
                    'Avg Relevance Score (%)': sum(metrics['relevance_scores']) / len(metrics['relevance_scores'])
                })
            
            df_comparison = pd.DataFrame(algo_comparison)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            fastest = df_comparison.loc[df_comparison['Avg Execution Time (ms)'].idxmin()]
            most_efficient = df_comparison.loc[df_comparison['Avg Comparisons'].idxmin()]
            highest_score = df_comparison.loc[df_comparison['Avg Relevance Score (%)'].idxmax()]
            
            with col1:
                st.metric("⚡ Fastest Algorithm", fastest['Algorithm'], f"{fastest['Avg Execution Time (ms)']:.3f} ms")
            
            with col2:
                st.metric("🎯 Most Efficient", most_efficient['Algorithm'], f"{int(most_efficient['Avg Comparisons'])} comparisons")
            
            with col3:
                st.metric("🏆 Highest Accuracy", highest_score['Algorithm'], f"{highest_score['Avg Relevance Score (%)']:.2f}%")
            
            st.divider()
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Execution time comparison
                fig_time = px.bar(
                    df_comparison,
                    x='Algorithm',
                    y='Avg Execution Time (ms)',
                    title='Average Execution Time Comparison',
                    color='Algorithm',
                    text_auto='.3f'
                )
                fig_time.update_layout(showlegend=False)
                st.plotly_chart(fig_time, use_container_width=True)
            
            with col2:
                # Comparisons comparison
                fig_comp = px.bar(
                    df_comparison,
                    x='Algorithm',
                    y='Avg Comparisons',
                    title='Average Character Comparisons',
                    color='Algorithm',
                    text_auto=True
                )
                fig_comp.update_layout(showlegend=False)
                st.plotly_chart(fig_comp, use_container_width=True)
            
            st.divider()
            
            # Relevance score comparison
            fig_score = px.bar(
                df_comparison,
                x='Algorithm',
                y='Avg Relevance Score (%)',
                title='Average Relevance Score by Algorithm',
                color='Algorithm',
                text_auto='.2f'
            )
            fig_score.update_layout(showlegend=False)
            st.plotly_chart(fig_score, use_container_width=True)
            
            st.divider()
            
            # Comparison table
            st.subheader("📊 Performance Metrics Table")
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
            # Insights
            st.subheader("💡 Key Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Time Efficiency:**")
                speedup = performance_metrics.calculate_speedup(
                    fastest['Avg Execution Time (ms)'],
                    df_comparison['Avg Execution Time (ms)'].max()
                )
                st.write(f"- Fastest algorithm is **{speedup}x faster** than slowest")
            
            with col2:
                st.write("**Comparison Efficiency:**")
                efficiency = most_efficient['Avg Comparisons'] / df_comparison['Avg Comparisons'].max() * 100
                st.write(f"- Most efficient algorithm uses **{efficiency:.1f}%** fewer comparisons")
            
        else:
            st.info("👈 Please complete the analysis first.")
    
    # Tab 5: Export Data
    with tab5:
        st.header("💾 Export Analysis Data")
        
        if 'analysis_complete' in st.session_state and st.session_state['analysis_complete']:
            cv_results = st.session_state['cv_results']
            df_results = performance_metrics.aggregate_results(cv_results)
            
            # Centered preview with adjustable number of rows
            left, center, right = st.columns([1, 4, 1])
            with center:
                st.subheader("📊 Preview")
                total_rows = int(len(df_results))
                default_rows = min(10, total_rows) if total_rows > 0 else 1
                rows_to_show = st.number_input(
                    "Rows to show",
                    min_value=1,
                    max_value=max(total_rows, 1),
                    value=default_rows,
                    step=1,
                    help="Select how many rows to display in the preview"
                )
                st.dataframe(df_results.head(int(rows_to_show)), use_container_width=True, hide_index=True)
                st.metric("Total Records", total_rows)
            
            st.divider()
            
            # Export options below the preview
            st.subheader("📄 Export Options")
            
            # CSV export
            csv_data = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name=f"cv_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # JSON export
            json_data = json.dumps(cv_results, indent=2)
            st.download_button(
                label="📥 Download Results as JSON",
                data=json_data,
                file_name=f"cv_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            # Save to results folder
            if st.button("💾 Save to Results Folder", use_container_width=True):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                # Save CSV
                csv_path = f"results/analysis_results_{timestamp}.csv"
                df_results.to_csv(csv_path, index=False)
                
                # Save JSON
                json_path = f"results/performance_summary_{timestamp}.json"
                with open(json_path, 'w') as f:
                    json.dump(cv_results, f, indent=2)
                
                st.success(f"✅ Results saved to `results/` folder!")
        
        else:
            st.info("👈 Please complete the analysis first to export data.")


if __name__ == "__main__":
    main()
# for python 
# pip install -r requirements.txt
# streamlit run app.py