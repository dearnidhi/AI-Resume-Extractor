import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="hr_tool_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS hr_tool_db")
    conn.commit()
    cursor.close()
    conn.close()

def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS candidates")  # Drop the existing table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        description TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploaded_cvs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        file_data LONGBLOB NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        experience VARCHAR(255),
        mobile VARCHAR(255),
        email VARCHAR(255),
        skills TEXT,
        education TEXT,
        summary TEXT,
        cv_name VARCHAR(255),
        action VARCHAR(50),
        match_score FLOAT NOT NULL 
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_to_db(dataframe):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    for _, row in dataframe.iterrows():
        # Handle the 'skills' field: If it's a list, join it; if it's empty or None, set it to a default value.
        skills = ', '.join(row['skills']) if isinstance(row['skills'], list) and row['skills'] else 'N/A'
        
        cursor.execute(
            """INSERT INTO candidates (name, experience, mobile, email, skills, education, summary, cv_name, action, match_score) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (row['Candidate name'], row['Experience'], row['Mobile Number'],
             row['Email'], skills, row['Education'],
             row['CV Summary'], row['CV Name'], row['Action'], row['Match Score'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def save_job_description(jd_text):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO job_descriptions (description) VALUES (%s)", (jd_text,))
    conn.commit()
    cursor.close()
    conn.close()

def save_uploaded_cv(file):
    conn = connect_to_db()
    cursor = conn.cursor()
    file_data = file.read()
    cursor.execute("INSERT INTO uploaded_cvs (file_name, file_data) VALUES (%s, %s)", (file.name, file_data))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_from_db(query, params=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Call these functions when initializing your app
create_db()  # Ensure the database exists
create_tables()  # Ensure the required tables exist
