
import sqlite3


DATABASE_NAME = "deadlines.db"


# Step 1: Create the database table
def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deadlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT,
            subject TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    connection.commit()

    connection.close()


# Step 2: Add a deadline without duplicates
def add_deadline(task, date, subject):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    # Normalize the task name
    clean_task = (
        task.strip()
        .replace("–", "-")
        .replace("—", "-")
        .replace(" ", "")
        .lower()
    )

    cursor.execute("""
        SELECT id, task, date, subject
        FROM deadlines
    """)

    existing_deadlines = cursor.fetchall()

    duplicate_found = False

    for saved_id, saved_task, saved_date, saved_subject in existing_deadlines:

        saved_clean_task = (
            saved_task.strip()
            .replace("–", "-")
            .replace("—", "-")
            .replace(" ", "")
            .lower()
        )

        if (
            saved_clean_task == clean_task
            and saved_date == date
            and saved_subject.strip().lower() == subject.strip().lower()
        ):
            duplicate_found = True
            break

    # Insert only if the deadline does not already exist
    if not duplicate_found:

        cursor.execute("""
            INSERT INTO deadlines (task, date, subject)
            VALUES (?, ?, ?)
        """, (task, date, subject))

        connection.commit()

    connection.close()


# Step 3: Retrieve all saved deadlines
def get_deadlines():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, task, date, subject, completed
        FROM deadlines
        ORDER BY date
    """)

    deadlines = cursor.fetchall()

    connection.close()

    return deadlines


# Step 5: Update deadline completion status
def update_deadline_status(deadline_id, completed):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE deadlines
        SET completed = ?
        WHERE id = ?
    """, (completed, deadline_id))

    connection.commit()

    connection.close()



# Step 4: Remove existing duplicate deadlines
def remove_duplicate_deadlines():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, task, date, subject
        FROM deadlines
        ORDER BY id
    """)

    all_deadlines = cursor.fetchall()

    seen_deadlines = set()

    for deadline_id, task, date, subject in all_deadlines:

        clean_task = (
            task.strip()
            .replace("–", "-")
            .replace("—", "-")
            .replace(" ", "")
            .lower()
        )

        clean_subject = subject.strip().lower()

        deadline_key = (clean_task, date, clean_subject)

        if deadline_key in seen_deadlines:

            cursor.execute("""
                DELETE FROM deadlines
                WHERE id = ?
            """, (deadline_id,))

        else:
            seen_deadlines.add(deadline_key)

    connection.commit()

    connection.close()

    print("Duplicate deadlines removed successfully!")


# Step 5: Create the database
create_database()

print("Database created successfully!")


def delete_deadline(deadline_id):
    conn = sqlite3.connect("deadlines.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM deadlines WHERE id = ?",
            (deadline_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print(f"Task {deadline_id} deleted successfully.")
            return True
        else:
            print(f"No task found with ID {deadline_id}.")
            return False

    except sqlite3.Error as error:
        conn.rollback()
        print(f"Database delete error: {error}")
        return False

    finally:
        conn.close()
