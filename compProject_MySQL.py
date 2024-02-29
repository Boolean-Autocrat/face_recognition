from tkinter import messagebox
import mysql.connector
from mysql.connector import errorcode
import os
from tkinter import *
from dotenv import load_dotenv

load_dotenv()


def taking_password():
    global pword
    global entry
    global PasswordWindow
    try:
        with open(
            os.path.dirname(os.path.realpath(__file__)) + "/MySQL_password.txt", "r"
        ) as file:
            pword = file.read()
    except FileNotFoundError:
        PasswordWindow = Tk()
        PasswordWindow.geometry("200x150")
        PasswordWindow.title("MySQL Password")
        label = Label(
            PasswordWindow,
            text="Enter MySQL password:",
            font=("times new roman", 13, "bold"),
        )
        label.pack()
        entry = Entry(PasswordWindow, width=20, font=("times new roman", 13, "bold"))
        entry.pack()
        button = Button(
            PasswordWindow,
            text="Enter",
            width=10,
            bg="blue",
            cursor="hand2",
            command=entering_password,
        )
        button.pack()
        # PasswordWindow.quit
        PasswordWindow.mainloop()

    return pword


def entering_password():
    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/MySQL_password.txt", "w"
    ) as file:
        file.write(entry.get())
        file.flush()
        # PasswordWindow.quit()
        taking_password()


def inserting_data(self):
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    my_cursor = mydb.cursor()

    my_cursor.execute("use {}".format(os.getenv("DB_NAME")))
    add_data = (
        "INSERT INTO new_student_info "
        "(Stream, Grade, Section, Year, Student_id, Name, Roll_No, Gender, Email, Phone, DOB, Photo_Sample) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (
        self.dep_combo.get(),
        int(self.grade_combo.get()),
        self.sec_combo.get(),
        self.year_combo.get(),
        int(self.studentId_entry.get()),
        self.studentName_entry.get(),
        int(self.roll_no_entry.get()),
        self.gender_entry.get(),
        self.email_entry.get(),
        int(1234567890),
        self.date_entry.get(),
        self.photo_sample.get(),
    )
    # add_data = ("INSERT INTO new_student_info "
    #        "(Stream, Grade, Section, Year, Student_id, Name, Roll_No, Gender, Email, Phone, DOB, Photo_Sample) "
    #        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    # data = (self.dep_combo.get(), int(self.grade_combo.get()), self.sec_combo.get(),
    #     self.year_combo.get(), int(self.studentId_entry.get()), self.studentName_entry.get(),
    #     int(self.roll_no_entry.get()), self.gender_entry.get(), self.email_entry.get(),
    #     "Constant",  # Placeholder for the constant phone number
    #     self.date_entry.get(), self.photo_sample.get())
    my_cursor.execute(add_data, data)
    mydb.commit()

    # my_cursor.execute("insert into new_student_info values ('{}', {}, '{}', '{}', {}, '{}', {}, '{}', '{}', '{}', '{}')".format(
    # 															self.dep_combo.get(),
    # 															int(self.grade_combo.get()),
    # 															self.sec_combo.get(),
    # 															self.year_combo.get(),
    # 															int(self.studentId_entry.get()),
    # 															self.studentName_entry.get(),
    # 															int(self.roll_no_entry.get()),
    # 															self.gender_entry.get(),
    # 															self.email_entry.get(),
    # 															self.date_entry.get(),
    # 															self.photo_sample.get()
    # 															))
    # mydb.commit()

    my_cursor.close()
    mydb.close()


def fetching_data(
    self,
):  # i've put the data in the list, "info" but it still has to go into the table using tkinter.
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    my_cursor = mydb.cursor()
    my_cursor.execute("select * from new_student_info")
    info = my_cursor.fetchall()
    my_cursor.close()
    mydb.close()

    return info


def deleting_data(self):
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    my_cursor = mydb.cursor()
    my_cursor.execute(
        "delete from new_student_info where Student_id = {}".format(
            self.var_roll.get(),
        )
    )
    my_cursor.commit()
    my_cursor.close()
    mydb.close()


def searching_data(self, search_field, search_val):
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    my_cursor = mydb.cursor()
    if search_field == "Name":
        my_cursor.execute(
            "select * from new_student_info where Name like '%{}%'".format(search_val)
        )
    elif search_field == "Roll No":
        my_cursor.execute(
            "select * from new_student_info where Roll_No like {}".format(search_val)
        )
    info = my_cursor.fetchall()
    my_cursor.close()
    mydb.close()

    return info


def completing_data(self, search_val):
    mydb = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    my_cursor = mydb.cursor()
    my_cursor.execute(
        "select Stream, Roll_No from new_student_info where Student_id = {}".format(
            search_val
        )
    )
    info = my_cursor.fetchall()
    my_cursor.close()
    mydb.close()

    return info
