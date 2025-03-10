import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


def page_config():
    st.set_page_config(page_title="CUIMS Clone", layout="wide")
    st.markdown("# CUIMS Clone")
    st.write('---')
    # with open('local_data/logs.json', 'r') as f:
    #     l_up = json.load(f)
    # col1, col2 = st.columns([9,2])
    # with col2:
    #     st.info(f"Last Updated on : {l_up['last_updated']}")

def show_attendance():
    try:
        with open('local_data/attendance.json', 'r') as f:
            attendance_data = json.load(f)
    except:
        return None

    total_attended = sum(int(record["Eligible Attended"]) for record in attendance_data)
    total_delivered = sum(int(record["Eligible Delivered"]) for record in attendance_data)
    overall_percentage = (total_attended / total_delivered * 100) if total_delivered > 0 else 0
    overall_color = "green" if overall_percentage > 75 else "red"

    st.write("## Attendance Details")

    st.markdown(
        f"""
        <div class="attendance-container" style='margin-top:2em; '>
            <span class="attendance-title">Overall Attendance</span>
            <div class="attendance-right">
                <span>Attended: {total_attended} / {total_delivered}</span><br>
                <span class="{overall_color}">{overall_percentage:.2f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .attendance-container {
            width: 100%;
            padding: 15px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .attendance-title {
            font-weight: bold;
            color: #2b8cf0;
            flex: 1;
        }
        .attendance-right {
            text-align: right;
            flex: 1;
        }
        .green { color: green; font-weight: bold; }
        .red { color: red; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True
    )

    mid = len(attendance_data) // 2
    col1, col2 = st.columns(2)

    for i, record in enumerate(attendance_data):
        title = record["Title"]
        attended = record["Eligible Attended"]
        delivered = record["Eligible Delivered"]
        percentage = float(record["Eligible Percentage"])
        color_class = "green" if percentage > 75 else "red"

        container_html = (
            f"<div class='attendance-container'>"
            f"<span class='attendance-title'>{title}</span>"
            f"<div class='attendance-right'>"
            f"<span>Attended: {attended} / {delivered}</span><br>"
            f"<span class='{color_class}'> {percentage}%</span>"
            f"</div></div>"
        )

        if i < mid:
            with col1:
                st.markdown(container_html, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(container_html, unsafe_allow_html=True)

def show_timetable():
    st.markdown("## Timetable")

    st.markdown(
        """
        <style>
        div[data-testid="stTabs"] button {
            flex-grow: 1;
            text-align: center;
        }
        .timetable-entry {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            padding: 10px;
            margin-bottom: 8px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
        }
        .time {
            font-weight: bold;
            font-size: 16px;
            color: #2b8cf0;
            flex: 1;
            text-align: left;
        }
        .details {
            flex: 2;
            text-align: right;
            font-size: 15px;
        }
        .location {
            font-size: 13px;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with open('local_data/time_table.json', 'r') as f:
        timetable_data = json.load(f)
    
    with open('local_data/subject_data.json', 'r') as f:
        course_list = json.load(f)

    course = {course_item["course_code"]: course_item["course_name"] for course_item in course_list}
    days_map = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}

    tabs = st.tabs(list(days_map.values()))

    for i, (day_number, day_name) in enumerate(days_map.items()):
        with tabs[i]:
            # st.markdown(f"#### {day_name}")
            for item in timetable_data[day_number - 1]:
                course_name = course.get(item['subject_code'], 'Unknown Course')
                st.markdown(
                    f"<div class='timetable-entry'>"
                    f"<div class='time'>{item['time']}</div>"
                    f"<div class='details'><b>{course_name}</b><br><span class='location'>{item['location']}</span></div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

def show_profile_imp_msg():

    st.write("## Student Profile")

    st.markdown(
        """
        <style>
        .profile-container {
            width: 100%;
            padding: 15px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .profile-key {
            font-weight: bold;
            color: #2b8cf0;
        }
        .profile-value {
            font-weight: normal;
            color: #333;
        }
        # .imp-msg {
        #     width: 100%;
        #     padding: 15px;
        #     border-left: 5px solid #f39c12;
        #     background: #fffbe6;
        #     border-radius: 5px;
        #     margin-bottom: 10px;
        # }
        </style>
        """,
        unsafe_allow_html=True
    )

    with open('local_data/profile.json', 'r') as f:
        profile_data = json.load(f)

    col11, col22 = st.columns([5,2])
    with col11:
        left_column = list(profile_data.items())[:7]
        right_column = list(profile_data.items())[8:15]

        col1, col2 = st.columns(2)

        with col1:
            for key, value in left_column:
                st.markdown(f"<div class='profile-container'><span class='profile-key'>{key}:</span> <span class='profile-value'>{value}</span></div>", unsafe_allow_html=True)

        with col2:
            for key, value in right_column:
                st.markdown(f"<div class='profile-container'><span class='profile-key'>{key}:</span> <span class='profile-value'>{value}</span></div>", unsafe_allow_html=True)

    with col22:
        with open('local_data/imp_msg.json', 'r') as f:
            imp_msg = json.load(f)

        st.write("## Important Message")
        st.info(imp_msg['msg'])
    st.write("---")

def show_courses():
    st.write("## Your Courses")

    with open('local_data/subject_data.json', 'r') as f:
        courses = json.load(f)

    st.markdown(
        """
        <style>
        .course-container {
            width: 100%;
            padding: 15px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .course-title {
            font-weight: bold;
            color: #2b8cf0;
        }
        .course-code {
            text-align: right;
            font-weight: bold;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for course in courses:
        st.markdown(
            f"<div class='course-container'>"
            f"<span class='course-title'>{course['course_name']}</span>"
            f"<span class='course-code'>{course['course_code']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

def show_result():
    st.write("## Academic Result")

    with open('local_data/result.json', 'r') as f:
        result_data = json.load(f)

    st.markdown(
        """
        <style>
        .result-container {
            width: 100%;
            padding: 12px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .result-title {
            font-weight: bold;
            color: #2b8cf0;
            flex: 1;
        }
        .result-value {
            text-align: right;
            font-weight: bold;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<div class='result-container'><span class='result-title'>Overall CGPA</span><span class='result-value'>{result_data['cgpa']}</span></div>", unsafe_allow_html=True)

    sgpa_data = [{"Semester": sem["semester"], "SGPA": sem["sgpa"]} for sem in result_data['semester_wise_result']]
    df = pd.DataFrame(sgpa_data)

    fig = px.line(df, x="Semester", y="SGPA", markers=True, title="SGPA Trend Across Semesters", height=250)
    st.plotly_chart(fig, use_container_width=True)

    semester_tabs = st.tabs([f"Semester {sem['semester']}" for sem in result_data['semester_wise_result']])

    for tab, semester in zip(semester_tabs, result_data['semester_wise_result']):
        with tab:
            # st.markdown(f"<div class='result-container'><span class='result-title'>SGPA</span><span class='result-value'>{semester['sgpa']}</span></div>", unsafe_allow_html=True)

            for subject in semester['semester_result']:
                st.markdown(
                    f"<div class='result-container'>"
                    f"<span class='result-title'>{subject['subject_name']}</span>"
                    f"<span class='result-value'>{subject['subject_grade_ob']} ({subject['subject_credits']} Credits)</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

def show_fees():
    st.markdown("## Fee Payment History")

    with open('local_data/fees.json', 'r') as f:
        fees_data = json.load(f)
    st.markdown(
        """
        <style>
        .fees-container {
            width: 100%;
            padding: 15px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .fees-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .fees-title {
            font-weight: bold;
            color: #2b8cf0;
        }
        .fees-status {
            font-weight: bold;
            text-align: right;
        }
        details {
            cursor: pointer;
            border: 1px solid #ddd;
            padding: 8px;
            border-radius: 5px;
            margin-bottom: 10px;
            background: transparent;
        }
        summary {
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            list-style: none;
        }
        summary::-webkit-details-marker {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(height=500):
        left_col, right_col = st.columns(2)

    for i, payment in enumerate(fees_data):
        status_color = "green" if payment['status'] == 'SUCCESS' else "red"
        fee_html = f"""
        <div class="fees-container">
            <details>
                <summary>
                    <div class="fees-header">
                        <span class="fees-title">{payment['payment_date']}</span>
                        <span class="fees-status" style="color: {status_color};">₹{float(payment['total_amt']):,.2f}  {payment['status']}</span>
                    </div>
                </summary>
                <div>
                    <p><b>Transaction Ref:</b> {payment['trans_ref_no']}</p>
                    <p><b>Bank Ref:</b> {payment['bank_ref_no']}</p>
                    <p><b>Payment Mode:</b> {payment['payment_mode']}</p>
                </div>
            </details>
        </div>
        """

        if i < len(fees_data) / 2:
            left_col.markdown(fee_html, unsafe_allow_html=True)
        else:
            right_col.markdown(fee_html, unsafe_allow_html=True)

def show_datesheet():
    st.markdown("## Examination Schedule")

    with open('local_data/datesheet.json', 'r') as f:
        datesheet = json.load(f)

    exam_types = sorted(set(exam['datesheet_type'] for exam in datesheet))
    tabs = st.tabs(exam_types)

    st.markdown(
        """
        <style>
        .exam-container {
            width: 100%;
            padding: 15px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .exam-left {
            font-weight: bold;
            color: #2b8cf0;
            flex: 1;
        }
        .exam-right {
            text-align: right;
            font-weight: bold;
            color: #333;
        }
        .exam-subtext {
            font-size: 0.9em;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for tab, exam_type in zip(tabs, exam_types):
        with tab:
            filtered_exams = sorted(
                [exam for exam in datesheet if exam['datesheet_type'] == exam_type],
                key=lambda x: datetime.strptime(x['exam_date'], '%d %b %Y')
            )

            if filtered_exams:
                for exam in filtered_exams:
                    venue = f"<a href='{exam['exam_venue']}' target='_blank'>LINK</a>" if exam['exam_venue'].startswith("https") else exam['exam_venue']
                    
                    st.markdown(
                        f"<div class='exam-container'>"
                        f"<div class='exam-left'>{exam['course_name']}<br><span class='exam-subtext'>{exam['course_code']}</span></div>"
                        f"<div class='exam-right'>{exam['exam_date']}<br><span class='exam-subtext'>{venue}</span></div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.write("No exams scheduled.")

def show_leaves():
    st.markdown("## Leave Applications")

    with open('local_data/leaves.json', 'r') as f:
        leaves_data = json.load(f)[0]  

    st.markdown(
        """
        <style>
        .leave-container {
            width: 100%;
            padding: 15px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .leave-left {
            font-weight: bold;
            color: #2b8cf0;
            flex: 1;
        }
        .leave-right {
            text-align: right;
            font-weight: bold;
            color: #333;
        }
        .leave-subtext {
            font-size: 0.9em;
            color: #555;
        }
        .approved { color: green; }
        .cancelled { color: red; }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.container(height=500):
        for leave in leaves_data:
            status_class = "approved" if "Approved" in leave['dl_status'] else "cancelled"
            
            st.markdown(
                f"<div class='leave-container'>"
                f"<div class='leave-left'>{leave['dl_category']}<br><span class='leave-subtext'>{leave['dl_type']}</span></div>"
                f"<div class='leave-right'>{leave['dl_date']}<br><span class='leave-subtext {status_class}'>{leave['dl_status']}</span></div>"
                f"</div>",
                unsafe_allow_html=True
            )

def show_marks():
    st.write("## Marks Overview")

    with open('local_data/marks.json', 'r') as f:
        marks_data = json.load(f)

    subjects = []
    percentages = []

    for subject, data in marks_data.items():
        total_marks = 0
        obtained_marks = 0

        for exp in data["experiments"]:
            marks = 0 if exp["marks_obtained"] == "ABSENT" else float(exp["marks_obtained"])
            total_marks += int(exp["max_marks"])
            obtained_marks += marks

        percentage = (obtained_marks / total_marks) * 100 if total_marks > 0 else 0
        subjects.append(subject)
        percentages.append(percentage)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=percentages, theta=subjects, fill='toself', marker=dict(color="#2b8cf0")))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=400, title="Overall Marks Percentage by Subject")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <style>
        .marks-container {
            width: 100%;
            padding: 10px;
            border-left: 5px solid #2b8cf0;
            background: #f0f8ff;
            border-radius: 5px;
            margin-bottom: 8px;
        }
        .marks-title {
            font-weight: bold;
            color: #2b8cf0;
        }
        .marks-value {
            font-weight: bold;
            color: #333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for subject, data in marks_data.items():
        with st.expander(subject):
            for exp in data["experiments"]:
                marks_obtained = exp["marks_obtained"]
                marks_color = "red" if marks_obtained == "ABSENT" else "black"

                st.markdown(
                    f"""
                    <div class='marks-container'>
                        <span class='marks-title'>{exp['name']}</span><br>
                        <span class='marks-value' style='color: {marks_color};'>{marks_obtained}/{exp['max_marks']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
