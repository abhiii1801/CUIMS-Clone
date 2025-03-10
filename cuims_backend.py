from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from PIL import Image
import time
import streamlit as st
from io import BytesIO
import google.generativeai as genai
import requests
import os
import json

def login_first(uid):
    print("\n[CUIMS BACKEND FIRST LOGIN]\n")
    if 'driver' not in st.session_state:
        chrome_options = Options()
        # chrome_options.add_argument("--headless") 
        st.session_state.driver = webdriver.Chrome(options=chrome_options)
        st.session_state.wait = WebDriverWait(st.session_state.driver, 10)

    driver = st.session_state.driver
    wait = st.session_state.wait

    driver.get('https://students.cuchd.in/frmMyCourse.aspx')

    user_input = wait.until(EC.presence_of_element_located((By.ID, "txtUserId")))
    user_input.send_keys(uid)

    next_button = driver.find_element(By.ID, "btnNext")
    next_button.click()

    try:
        captcha_im = wait.until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
        captcha_image = captcha_im.screenshot_as_png
        image = Image.open(BytesIO(captcha_image))
        return image
        
    except NoSuchElementException:
        return False
    
def login_second(password, captcha):
    print("\n[CUIMS BACKEND SECOND LOGIN]\n")
    try:
        driver = st.session_state.driver
        wait = st.session_state.wait
        pass_input = driver.find_element(By.ID, "txtLoginPassword")
        pass_input.send_keys(password)

        captcha_input = driver.find_element(By.ID, "txtcaptcha")
        captcha_input.send_keys(captcha)

        next_button = driver.find_element(By.ID, "btnLogin")
        next_button.click()

        return True
    except:
        return False

def check_login():
    print("\n[CUIMS BACKEND CHECK LOGIN]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait
    driver.refresh()
    try:
        err_dialog = WebDriverWait(st.session_state.driver, 2).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]')))
        err_dialog_state = err_dialog.get_attribute('style')
        if "display: none" in err_dialog_state:
            print('No error displayed')
            return True
        else:
            reason = err_dialog.find_element(By.TAG_NAME, 'p').text
            if reason == 'Invalid Captcha':
                st.toast("Captcha validation failed! Trying again. 🐷")
                err_dialog.find_element(By.XPATH, '//*[@id="login-page"]/div/div[2]/button[2]').click()

                captcha_im = wait.until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
                captcha_image = captcha_im.screenshot_as_png
                st.session_state.first_login_success = Image.open(BytesIO(captcha_image))
                return -2
            else:
                captcha_im = wait.until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
                captcha_image = captcha_im.screenshot_as_png
                st.session_state.first_login_success = Image.open(BytesIO(captcha_image))
                    
                err_dialog.find_element(By.XPATH, '//*[@id="login-page"]/div/div[2]/button[2]').click()
                return -1
    except:
        return True

def extract_text_from_image(image):
    st.session_state.captcha_tries += 1
    try:
        genai.configure(api_key='')
        model = genai.GenerativeModel("gemini-1.5-flash")

        if isinstance(image, bytes):
            image = Image.open(BytesIO(image))

        prompt = "Extract the text from this image and return only the text in mind that the capitalisation matter also dont add any space bw the characters, this is a 4 character captcha that is needed to be detected"

        response = model.generate_content([prompt, image])
        return response.text
    except:
        st.session_state.captcha_tries = 5

def retrive_imp_msg():
    print("\n[CUIMS BACKEND RETRIVE IMP MSGS]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait
    try:
        driver.get("https://students.cuchd.in/StudentHome.aspx")
        msg = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[3]/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li/p/span').text
        return msg
    except:
        return False

def retrive_courses():
    print("\n[CUIMS BACKEND RETRIVE COURSES]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait

    driver.get('https://students.cuchd.in/frmMyTimeTable.aspx')

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    courses = []

    try:
        courses_table = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[4]/div[3]/div/div[4]/div/table/tbody')))

        table_data = courses_table.find_elements(By.TAG_NAME, 'tr')
        for row in table_data[1:]:
            courses_data = {}
            row_data = row.find_elements(By.TAG_NAME, 'td')

            courses_data["course_code"] = row_data[0].text
            courses_data["course_name"] = row_data[1].text
            courses.append(courses_data)

        return courses
    except:
        return False
    
def retrive_timetable():
    print("\n[CUIMS BACKEND RETRIVE TIMETABLE]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait

    final_time_table = []

    try:
        timetable = {
                0: [],
                1: [],
                2: [],
                3: [],
                4: [],
                5: [],
                6: []
        }

        timetable_table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_grdMain"]/tbody'))).find_elements(By.TAG_NAME, 'tr')

        for row_index, row in enumerate(timetable_table[1:]):
            rows = row.find_elements(By.TAG_NAME, 'td')
            for col_index, val in enumerate(rows[1:]):
                course_data = val.text

                if course_data.strip():
                    course_data_with_time = f"{course_data} on {rows[0].text}"

                    timetable[col_index].append(course_data_with_time)
        
        for day, val in timetable.items():
            day_data = []
            for period in val:
                period_data = {}
                period = period.split('::')
                subject = period[0].split(':')[0]
                teacher_data = period[1].split("By ")[1].split(" at ")
                if len(teacher_data)>1:
                    teacher = teacher_data[0]
                    class_loc = teacher_data[1].split("on")
                else:
                    teacher = ""
                    class_loc = teacher_data[0].split("at ")[1].split(" on ")
                period_data['subject_code'] = subject
                period_data['teacher'] = teacher
                period_data['location'] = class_loc[0]
                period_data['time'] = class_loc[1]
                period_data['day_number'] = day+1

                day_data.append(period_data)
            final_time_table.append(day_data)

        return final_time_table
    except Exception as e:
        print(f"Error retrieving timetable: {e}")
        return False
    
def retrive_attendance():
    print("\n[CUIMS BACKEND RETRIVE ATTENDANCE]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait
    driver.get('https://students.cuchd.in/frmStudentCourseWiseAttendanceSummary.aspx?type=etgkYfqBdH1fSfc255iYGw==')

    time.sleep(2)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        attendance_table = wait.until(EC.visibility_of_element_located((By.ID, 'SortTable')))
        table_data = attendance_table.find_element(By.XPATH, '//*[@id="SortTable"]/tbody').find_elements(By.TAG_NAME, 'tr')

        attendance_data = []
        for row in table_data:
            td = row.find_elements(By.TAG_NAME, 'td')
            attendance_dict = {
                'Course Code' : td[0].text,
                'Title' : td[1].text,
                'Eligible Delivered' : td[8].text,
                'Eligible Attended' : td[9].text,
                'Eligible Percentage' : td[10].text
            }
            attendance_data.append(attendance_dict)

        
        return attendance_data
    except:
        return False
    
def retrive_leaves():
    print("\n[CUIMS BACKEND RETRIVE LEAVES]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait
    leaves = []
    try:
        driver.get('https://students.cuchd.in/frmStudentApplyDutyLeave.aspx')
        dl = []
        tab = wait.until(EC.visibility_of_element_located((By.ID, "__tab_Tab3")))
        tab.click()
        dl_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[3]/div/div[5]/table/tbody/tr[1]/td/div/div/div/div[2]/div[3]/div/div/div/table/tbody').find_elements(By.TAG_NAME, 'tr')
        try:
            for row in dl_table[1:]:
                row = row.find_elements(By.TAG_NAME, 'td')
                dl_info = {}
                dl_info['dl_number'] = row[1].text
                dl_info['dl_timing'] = row[2].text
                dl_info['dl_category'] = row[3].text
                dl_info['dl_type'] = row[5].text
                dl_info['dl_date'] = row[6].text
                dl_info['dl_status'] = row[7].text
                dl.append(dl_info)
            
            leaves.append(dl)
        except:
            leaves.append(dl)
            pass
        
        # driver.get('https://students.cuchd.in/frmStudentMedicalLeaveApply.aspx')
        # ml = []
        # tab = wait.until(EC.visibility_of_element_located((By.ID, "__tab_Tab3")))
        # tab.click()
        # ml_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[3]/div/div[5]/table/tbody/tr[1]/td/div/div/div/div[2]/div[3]/div/div/div/table/tbody').find_elements(By.TAG_NAME, 'tr')
        # for row in ml_table[1:]:
        #     row = row.find_elements(By.TAG_NAME, 'td')
        #     ml_info = {}
        #     ml_info['dl_number'] = row[1].text
        #     ml_info['dl_timing'] = row[2].text
        #     ml_info['dl_category'] = row[3].text
        #     ml_info['dl_type'] = row[5].text
        #     ml_info['dl_date'] = row[6].text
        #     ml_info['dl_status'] = row[7].text
        #     ml.append(ml_info)
        return leaves

    except:
        return False

def retrive_datesheet():
    print("\n[CUIMS BACKEND RETRIVE DATESHEET]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait
    try:
        driver.get('https://students.cuchd.in/frmStudentDatesheet.aspx')
        datesheet = []
        try:
            datesheet_table = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[4]/div[3]/div/div[2]/div[4]/div/div/div/table/tbody'))).find_elements(By.TAG_NAME, 'tr')
            for row in datesheet_table[1:]:
                row_data = {}
                row = row.find_elements(By.TAG_NAME, 'td')
                row_data['exam_type'] = row[0].text
                row_data['datesheet_type'] = row[1].text
                row_data['course_code'] = row[2].text
                row_data['course_name'] = row[3].text
                row_data['slot_no'] = row[4].text
                row_data['exam_date'] = row[7].text
                row_data['exam_time'] = row[8].text 
                venue_cell = row[9]
                link = venue_cell.find_elements(By.TAG_NAME, 'a')
                if link:
                    row_data['exam_venue'] = link[0].get_attribute('href')
                else:
                    row_data['exam_venue'] = venue_cell.text
                
                datesheet.append(row_data)
        except:
            pass

        return datesheet

    except:
        return False

def retrive_result():
    print("\n[CUIMS BACKEND RETRIVE RESULT]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait

    try:
        driver.get('https://students.cuchd.in/result.aspx')
        result = {}
        try:
            cgpa = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[4]/div[3]/div/div[2]/div[3]/div[2]/div[1]/div[5]/span'))).text
            result['cgpa'] = cgpa
            result['semester_wise_result'] = []

            results = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_wucResult1_dlResult"]/tbody').find_elements(By.XPATH, 'tr')
            for i, sem in enumerate(results):
                semester_res = {}
                semester_res['semester'] = sem.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_wucResult1_dlResult_lblSem_{i}"]').text
                semester_res['sgpa'] = sem.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_wucResult1_dlResult_div_sticky_{i}"]/span[3]').text.split(":")[1].strip()
                sem_res = sem.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_wucResult1_dlResult_Repeater1_{i}"]/tbody').find_elements(By.TAG_NAME, 'tr')
                semester_res['semester_result'] = []
                for row in sem_res[1:]:
                    sem_res_value = {}
                    col = row.find_elements(By.TAG_NAME, 'td')
                    sem_res_value['subject_code'] = col[0].text
                    sem_res_value['subject_name'] = col[1].text
                    sem_res_value['subject_credits'] = col[2].text
                    sem_res_value['subject_grade_ob'] = col[3].text
                    semester_res['semester_result'].append(sem_res_value)
                result['semester_wise_result'].append(semester_res)
        except:
            pass

        return result

    except:
        return False

def retrive_profile():
    print("\n[CUIMS BACKEND RETRIVE PROFILE]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait

    try:
        driver.get('https://students.cuchd.in/frmStudentProfile.aspx')
        personal_info = {}

        personal_info_table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'stuProfileData'))).find_element(By.CLASS_NAME, 'row')

        columns = personal_info_table.find_elements(By.CLASS_NAME, 'col-md-5.col-xs-6')
        for column in columns:
            rows = column.find_elements(By.CLASS_NAME, 'row')
            for row in rows:
                key = row.find_element(By.CLASS_NAME, 'col-sm-4').text.strip()
                value = row.find_element(By.CLASS_NAME, 'col-sm-8').text.strip()
                personal_info[key] = value
        
        education_info = []
        try:
            education_table = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_gvStudentQualification"]/tbody').find_elements(By.TAG_NAME, 'tr')
            for row in education_table[1:]:
                col_data = {}
                col = row.find_elements(By.TAG_NAME, 'td')
                col_data['qualification'] = col[0].text
                col_data['steram'] = col[1].text
                col_data['school/college'] = col[2].text
                col_data['university/board'] = col[3].text
                col_data['passing_year'] = col[4].text
                education_info.append(col_data)
        except:
            pass
        personal_info['education_info'] = education_info

        contact_info = []
        try:
            contact_table = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_gvStudentContacts"]/tbody').find_elements(By.TAG_NAME, 'tr')
            for row in contact_table[1:]:
                col_data = {}
                col = row.find_elements(By.TAG_NAME, 'td')
                col_data['contact_type'] = col[0].text
                col_data['residence'] = col[1].text
                col_data['office'] = col[2].text
                col_data['mobile'] = col[3].text
                col_data['email_id'] = col[4].text
                contact_info.append(col_data)
        except:
            pass
        personal_info['contact_info'] = contact_info

        return personal_info
        
    except Exception as e:
        print(f"Error: {e}")

def retrive_fee():
    print("\n[CUIMS BACKEND RETRIVE FEES]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait

    driver.get('https://students.cuchd.in/frmAccountStudentDetails.aspx')
    try:
        tab = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_RadTabStrip1"]/div/ul/li[2]/a/span/span/span')))
        tab.click()
        payments = []

        payment_table = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[3]/div/div[3]/div/div/div[2]/div[2]/table/tbody/tr[2]/td/div').find_elements(By.TAG_NAME, 'table')
        for table in payment_table:
            trans_detail = {}
            table = table.find_element(By.TAG_NAME, 'tbody').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'td')
            trans_detail['payment_date'] = table[0].text.replace('\n', ' ')
            col2 = table[1].find_elements(By.TAG_NAME, 'div')
            trans_detail['trans_ref_no'] = col2[0].find_elements(By.TAG_NAME, 'span')[1].text
            trans_detail['bank_ref_no'] = col2[1].find_elements(By.TAG_NAME, 'span')[1].text
            trans_detail['payment_mode'] = col2[2].find_elements(By.TAG_NAME, 'span')[1].text
            
            col3 = table[2].find_elements(By.TAG_NAME, 'div')
            trans_detail['total_amt'] = col3[0].text.split("Rs")[1].strip()
            trans_detail['service_tax'] = col3[1].text.split("Rs.")[1].strip()
            trans_detail['processing fee'] = col3[2].text.split("Rs.")[1].strip()

            trans_detail['status'] = table[3].text

            payments.append(trans_detail)


        return(payments)
    except:
        return False

def retrive_marks():
    print("\n[CUIMS BACKEND RETRIEVE MARKS]\n")
    driver = st.session_state.driver
    wait = st.session_state.wait

    driver.get('https://students.cuchd.in/frmStudentMarksView.aspx')

    subjects = {}
    accordion_headers = driver.find_elements(By.CLASS_NAME, "ui-accordion-header")

    for i,header in enumerate(accordion_headers):
        subject_text = header.text.strip()
        subjects[subject_text] = {"experiments": []}
        if i!=0:
            header.click()
            time.sleep(1) 
        
        current_panel_id = header.get_attribute("aria-controls")
        current_panel = driver.find_element(By.ID, current_panel_id)
        
        rows = current_panel.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 3:
                subjects[subject_text]["experiments"].append({
                    "name": cols[0].text.strip(),
                    "max_marks": cols[1].text.strip(),
                    "marks_obtained": cols[2].text.strip()
                })
    driver.close()
    return subjects

