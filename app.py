import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
st.set_page_config(
    page_title="Student Semester Performance Analysis",
    layout="wide"
)
st.title("🎓 Student Semester-wise Performance Analysis")
st.write("AI Minor Project | Pandas • NumPy • Matplotlib • Streamlit")
@st.cache_data
def load_data():
    return pd.read_csv("studentdata.csv")
df = load_data()
semester_cols = ['Sem1', 'Sem2', 'Sem3']
df[semester_cols] = df[semester_cols].apply(pd.to_numeric)
semester_mean = df[semester_cols].mean()
total_students = len(df)
highest_score = df[semester_cols].max().max()
lowest_score = df[semester_cols].min().min()
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Go to section:",
    [
        "Dataset Summary",
        "Student-wise Analysis",
        "Semester Trend",
        "Marks Histogram",
        "Download Report"
    ]
) 
if section == "Dataset Summary":
    st.subheader("📋 Dataset Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Highest Score", highest_score)
    col3.metric("Lowest Score", lowest_score)
    col4.metric("Overall Avg Score", round(semester_mean.mean(), 2))
    st.subheader("Semester-wise Average Marks")
    st.dataframe(semester_mean)
elif section == "Student-wise Analysis":
    st.subheader("👤 Student-wise Performance Analysis")
    student_id = st.text_input(
        "Enter Student ID (e.g., S1, S100, S500)"
    )
    if st.button("Analyze Student"):
        student_row = df[df['Student_ID'] == student_id]
        if student_row.empty:
            st.error("Student ID not found.")
        else:
            marks = student_row[semester_cols].values.flatten()
            st.write("### Marks")
            st.write({
                "Sem1": marks[0],
                "Sem2": marks[1],
                "Sem3": marks[2]
            })
            fig, ax = plt.subplots()
            ax.plot(semester_cols, marks, marker='o')
            ax.set_xlabel("Semester")
            ax.set_ylabel("Marks")
            ax.set_title(f"Performance of {student_id}")
            ax.grid(True)
            st.pyplot(fig)
            plt.close(fig)
elif section == "Semester Trend":
    st.subheader("📈 Semester-wise Performance Trend")
    fig, ax = plt.subplots()
    ax.plot(semester_mean.index, semester_mean.values, marker='o')
    ax.set_xlabel("Semester")
    ax.set_ylabel("Average Marks")
    ax.set_title("Semester-wise Average Performance")
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)
elif section == "Marks Histogram":
    st.subheader("📊 Marks Distribution Across Semesters")
    fig, ax = plt.subplots()
    ax.hist(df['Sem1'], bins=10, alpha=0.5, label='Sem1')
    ax.hist(df['Sem2'], bins=10, alpha=0.5, label='Sem2')
    ax.hist(df['Sem3'], bins=10, alpha=0.5, label='Sem3')
    ax.set_xlabel("Marks")
    ax.set_ylabel("Number of Students")
    ax.set_title("Score Distribution")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)
elif section == "Download Report":
    st.subheader("⬇️ Download Student Performance Report")
    df['Average_marks'] = df[semester_cols].mean(axis=1)
    df['Total_marks'] = df[semester_cols].sum(axis=1)
    df['Growth_Percentage'] = ((df['Sem3'] - df['Sem1']) / df['Sem1']) * 100
    report_df = df[
        ['Student_ID', 'Sem1', 'Sem2', 'Sem3',
         'Average_marks', 'Total_marks', 'Growth_Percentage']
    ]
    os.makedirs("output", exist_ok=True)
    report_path = "output/student_performance_report.csv"
    report_df.to_csv(report_path, index=False)
    st.success("Report generated successfully")
    with open(report_path, "rb") as f:
        st.download_button(
            label="Download CSV Report",
            data=f,
            file_name="student_performance_report.csv",
            mime="text/csv"
        )
