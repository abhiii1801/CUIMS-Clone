import streamlit as st
import cuims_backend
import time
import pandas as pd
import json
from datetime import datetime
import streamlit.components.v1 as components
import ui
import os

def get_uid_pass():
    with open("local_data/auth.json", "r") as file:
        auth_data = json.load(file)
        if auth_data["uid"] and auth_data["password"]:
            return (auth_data["uid"], auth_data["password"])
        else:
            return None

def login_page():
    with st.form(key='login_first'):
        st.subheader("Login")
        uid = st.text_input("Enter your UID: ")
        password = st.text_input("Enter your password:", type="password")
        #@ABhinav1818
        st.session_state.uid = uid
        st.session_state.password = password
        submit = st.form_submit_button("Login")
        if submit:
            login_first = cuims_backend.login_first(uid)
            if login_first:
                st.session_state.first_login_success = login_first
                st.success("First login successful! Proceed with Captcha.")
                # time.sleep(2)
                st.rerun()

def captcha_submission(captcha_text):
    # st.subheader("Captcha Submission")
    # with st.form(key='login_second'):
    #     st.image(st.session_state.first_login_success, width=200)
    #     captcha_text = st.text_input("Enter Captcha: ")
    #     submit_captcha = st.form_submit_button("Submit Captcha")
    #     if submit_captcha:
    print('Captcha Found : ' , captcha_text)
    success = cuims_backend.login_second(st.session_state.password ,captcha_text)
    if success == True:
        with open('local_data/auth.json', 'w') as file:
            json.dump({"uid" : st.session_state.uid, "password": st.session_state.password}, file)
                    
        logged_in = cuims_backend.check_login()
        if logged_in == True:
            st.session_state.logged_in = True
            st.toast("Logged In Successfully")
            time.sleep(2)
            st.rerun()
        elif logged_in == -2:
            st.toast("Captcha validation failed! Trying again. 🐷")
            time.sleep(2)
            st.session_state.pop('first_login_success')
            st.rerun()
        elif logged_in == -1:
            st.toast("Invalid Password. Please Login again to Continue.")
            with open('local_data/auth.json', 'w') as file:
                json.dump({"uid": "", "password": ""}, file)
            time.sleep(2)
            st.session_state.pop('first_login_success')
            st.rerun()

def retrive_data():
    print("[CUIMS BACKEND RETRIVE DATA]")

    imp_msg = cuims_backend.retrive_imp_msg()
    if imp_msg:
        with open('local_data/imp_msg.json', 'w') as file:
            json.dump({"msg": imp_msg}, file, indent=4)
        st.toast("Important Msgs saved successfully! 🙀")
    else:
        st.toast("Error with Important Message 🐷")

    courses = cuims_backend.retrive_courses()
    if courses:
        with open('local_data/subject_data.json', 'w') as file:
            json.dump(courses, file, indent=4)
        st.toast("Courses data saved successfully! 🙀")
    else:
        st.toast("Error with Courses 🐷")

    timetable_data = cuims_backend.retrive_timetable()
    if timetable_data:
        with open('local_data/time_table.json', 'w') as file:
            json.dump(timetable_data, file, indent=4)
        st.toast("Timetable data saved successfully! 🙀")
    else:
        st.toast("Error with Timetable 🐷")

    attendance_data = cuims_backend.retrive_attendance()
    if attendance_data:
        with open('local_data/attendance.json', 'w') as file:
            json.dump(attendance_data, file, indent=4)
        st.toast("Attendance data saved successfully! 🙀")
    else:
        st.toast("Error with Attendance 🐷")

    leaves_data = cuims_backend.retrive_leaves()
    if leaves_data:
        with open('local_data/leaves.json', 'w') as file:
            json.dump(leaves_data, file, indent=4)
        st.toast("Leaves data saved successfully! 🙀")
    else:
        st.toast("Error with Leaves 🐷")

    datesheet_data = cuims_backend.retrive_datesheet()
    if datesheet_data:
        with open('local_data/datesheet.json', 'w') as file:
            json.dump(datesheet_data, file, indent=4)
        st.toast("Datesheet data saved successfully! 🙀")
    else:
        st.toast("Error with Datesheet 🐷")

    results_data = cuims_backend.retrive_result()
    if results_data:
        with open('local_data/result.json', 'w') as file:
            json.dump(results_data, file, indent=4)
        st.toast("Results data saved successfully! 🙀")
    else:
        st.toast("Error with Results 🐷")

    profile_data = cuims_backend.retrive_profile()
    if profile_data:
        with open('local_data/profile.json', 'w') as file:
            json.dump(profile_data, file, indent=4)
        st.toast("Profile data saved successfully! 🙀")
    else:
        st.toast("Error with Profile 🐷")

    fee_data = cuims_backend.retrive_fee()
    if fee_data:
        with open('local_data/fees.json', 'w') as file:
            json.dump(fee_data, file, indent=4)
        st.toast("Fee Data saved successfully! 🙀")
    else:
        st.toast("Error with Fees 🐷")

    marks = cuims_backend.retrive_marks()
    if marks:
        with open('local_data/marks.json', 'w') as file:
            json.dump(marks, file, indent=4)
        st.toast("Marks Data saved successfully! 🙀")
    else:
        st.toast("Error with Marks 🐷")
    
    st.toast("All Data Retrived and Saved to JSON Files 🙀")

    time.sleep(2)

    with open('local_data/logs.json', 'w') as f:
        json.dump({"last_updated" : f"{str(datetime.now().strftime('%H:%M'))} on {str(datetime.now().strftime('%d/%m/%Y'))}"}, f)


    st.session_state.data_retrived = True
    st.rerun()

def check_auth():
    with open("local_data/auth.json", "r") as file:
        auth_data = json.load(file)
        if auth_data["uid"] and auth_data["password"]:
            if auth_data['uid']!="" and auth_data['password']!="":
                return True
            else:
                return False
        else:
            return False

def main():
    try:
        if(check_auth()):
            ui.page_config()

            col1,mar,col2 = st.columns([6,0.5,8])
            with col1:
                ui.show_attendance()
            with col2:
                ui.show_timetable()

            st.write('---')

            col1 ,mar, col2 = st.columns([8,0.5,5])
            with col1:
                ui.show_marks()
            with col2:
                ui.show_result()

            st.write('---')

            ui.show_profile_imp_msg()

            col1, col2 = st.columns(2)
            with col1:
                ui.show_fees()
            with col2:
                ui.show_leaves()
        else:
            login_page()
    except:
        login_page()

    if 'captcha_tries' not in st.session_state:
        st.session_state.captcha_tries = 0

    if 'logged_in' not in st.session_state or st.session_state.logged_in == False:
        if 'first_login_success' not in st.session_state:
            st.toast("Logging you in 🙀")
            uid_pass = get_uid_pass()
            if uid_pass is not None:
                st.session_state.uid = uid_pass[0]
                st.session_state.password = uid_pass[1]
                login_first = cuims_backend.login_first(uid_pass[0])
                if login_first:
                    st.session_state.first_login_success = login_first
                    time.sleep(1)
                    st.rerun()
                else:
                    login_page()
            else:
                st.toast("User Credentials not Found\n Please Login to Continue 🐷")
                login_page()
        else:
            if st.session_state.captcha_tries <4:
                captcha_text = cuims_backend.extract_text_from_image(st.session_state.first_login_success)
                st.toast(f"Filling in Captcha 🙀 Tries Count:{st.session_state.captcha_tries}")
                captcha_submission(captcha_text)
            else:
                st.toast("Captcha Detection Failed 🐷 PLease scroll down to fill Manually")
    else:
        if 'data_retrived' not in st.session_state or st.session_state.data_retrived == False:
            retrive_data()
            st.session_state.driver.close()

if __name__ == '__main__':
    main()

