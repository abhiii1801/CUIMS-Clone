# CUIMS Automation Dashboard

This project automates CUIMS login and data extraction using **Selenium** for web automation, **Google Gemini API** for CAPTCHA solving, and **Streamlit** for visualization. It retrieves student details, attendance, exam schedules, and results, presenting them in an interactive UI.

## Features

### 1. AI-Powered CAPTCHA Solving
- Uses **Google Gemini API** to extract text from the CAPTCHA image.
- If the AI fails, the CAPTCHA is displayed for **manual input**.

### 2. Web Automation & Data Extraction
- Uses **Selenium WebDriver** to navigate CUIMS pages and extract:
  - **Courses & Timetable**
  - **Attendance Summary**
  - **Results & Marks**
  - **Exam Datesheet**
  - **Fee Payment History**
  - **Important Announcements**
- Extracted data is saved as **JSON files** for efficient retrieval.

### 3. Data Processing & Storage
- **Session State Management** in Streamlit prevents repeated logins.
- **Local JSON Storage** reduces redundant data fetching.
- Uses **structured dictionaries** for data handling.

### 4. Interactive Data Visualization
- Attendance and results are displayed using **Plotly graphs**.
- **Color-coded indicators** highlight important insights (e.g., low attendance).
- Data is structured into **separate UI components** for clarity.

---

## Screenshots
![image](https://github.com/user-attachments/assets/f584b025-eabd-40be-87a6-fb7ec7fcf0a2)
![image](https://github.com/user-attachments/assets/f1985f0b-863f-4b8f-8265-1d6fdfa0e624)
![image](https://github.com/user-attachments/assets/b4c1731a-54a6-499f-adcf-50f8ec919259)

## How It Works

https://github.com/user-attachments/assets/de735ae0-c748-4ae5-80cd-901988ac2b2c

### Step 1: Authentication & CAPTCHA Handling
1. **User credentials** are read from `local_data/auth.json` or entered manually.
2. Selenium launches a **headless Chrome instance** and navigates to CUIMS.
3. If a CAPTCHA is detected:
   - It is **screenshot and processed** using Google Gemini API.
   - The AI-generated response is entered into the CAPTCHA field.
   - If AI fails, the CAPTCHA is shown to the user for manual input.
4. After submitting credentials, **login verification** checks for errors.

### Step 2: Data Retrieval
1. Once logged in, Selenium navigates through different CUIMS sections.
2. **Web scraping methods** extract table data for:
   - Attendance
   - Timetable
   - Exam schedules
   - Fee transactions
   - Academic results
3. Data is **cleaned and structured into JSON files** (`local_data/`).

### Step 3: Data Processing & Visualization
1. **Attendance Data**
   - Calculates **total attended vs. delivered lectures**.
   - Uses **color-coded warnings** for attendance below 75%.
   - Displays an **interactive bar chart**.

2. **Exam & Results Data**
   - Fetches **semester-wise SGPA & CGPA**.
   - Generates a **line chart** for performance trends.
   - Displays **marks per subject**.

3. **Timetable**
   - Extracts **daily schedule** and displays it in a structured layout.

4. **Fee Payment History**
   - Fetches transactions and categorizes **paid vs. pending** fees.

### Step 4: UI & Streamlit Components
- The **main UI (`new_app.py`)** loads the necessary components and JSON data.
- **Dynamic components**:
  - `show_attendance()`: Displays attendance stats with alerts.
  - `show_timetable()`: Organizes timetable data.
  - `show_result()`: Plots SGPA trends.
  - `show_marks()`: Lists subject-wise marks.
- **Session Management**
  - `st.session_state` ensures **login persistence** and prevents re-fetching data unnecessarily.

### Step 5: Secure Logout & Cleanup
1. Once data is retrieved, the **WebDriver session is closed**.
2. The **stored JSON files remain available** for the next session.
3. If a user manually logs out, the **local authentication file is cleared**.

---

## Requirements
- Python 3.x
- **Selenium** (Web Scraping & Automation)
- **Streamlit** (Frontend UI)
- **Google Gemini API** (CAPTCHA Processing)
- **Plotly** (Graphs & Visualizations)
- Pandas, Requests, PIL (Data Handling)
