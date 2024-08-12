# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Rebecca Bergh,8/12/2024,Added classes, properties and setters; removed duplicate errors
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"
EXIT_MSG: str = '''

    ╔════════════════ « ♦ » ═══╗
          Closing program...    
    ╚═══ « ♦ » ════════════════╝
'''


# ╔══ CLASS SECTION ═════════════════════════════════╗

# Person Class
class Person:
    """
    A class representing Person data with:
    Properties:
        first_name (str): Student's first name
        last_name (str): Student's last name
    ChangeLog:
        RebeccaBergh,8/12/2024,Created class
    Inherited by:
        Student class
    """

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        if value.isalpha():
            self.__first_name = value
        else:
            raise ValueError('The first name can only be alphabetic')

    @property
    def last_name(self) -> str:
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        if value.isalpha():
            self.__last_name = value
        else:
            raise ValueError('The last name can only be alphabetic')

    def __str__(self):
        """
        The string function for Person
        :return: The string value as csv
        """
        return f'{self.first_name}, {self.last_name}'


class Student(Person):
    """
    A class representing Student data with:
    Inherited properties (Person):
        first_name (str): Student's first name
        last_name (str): Student's last name
    Properties:
        course_name (str): Student's course name
    """

    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        return self.__course_name.title()

    @course_name.setter
    def course_name(self, value: str) -> None:
        # Make sure course name has space between name and number
        if " " in value:
            self.__course_name = value
        else:
            raise ValueError('The course name must be formatted with a space (i.e. Python 100)')

    def __str__(self) -> str:
        return f'{super().__str__()}, {self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list[Student]) -> list[Student]:
        """ This function reads data from a json file and loads it into a list of dictionary rows,
        then converts the dictionary rows into the custom Student object

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        RebeccaBergh,8/12/2024,Loaded json into dictionary rows; added FileNotFoundError

        :param file_name: string data with name of file to read from
        :param student_data: list of dictionary rows to be filled with file data

        :return: list
        """
        file_data = []
        file = None

        try:
            file = open(file_name, "r")
            file_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Error: The file does not exist.", e)
            file = open(file_name, 'w')
            print("Creating the file...")
            file.close()
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with reading the file.", e)
        finally:
            if not file.closed and file is not None:
                file.close()
        for row in file_data:
            student_data.append(
                Student(first_name=row["FirstName"],
                        last_name=row["LastName"],
                        course_name=row['CourseName'])
            )
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[Student]):
        """ This function first converts the custom Student object into a list
         of dictionary rows, then writes those rows to a json file

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """
        # Convert Student object data into dictionary rows
        file_data: list[dict:str, str] = []
        for student in student_data:
            file_data.append({'FirstName': student.first_name,
                              'LastName': student.last_name,
                              'CourseName': student.course_name})
        file = None
        # write dictionary rows into JSON and display to end user
        try:
            file = open(file_name, "w")
            json.dump(file_data, file, indent=1)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        # close file if not already
        finally:
            if not file.closed and file is not None:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list[Student]):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'{student.first_name} {student.last_name} is enrolled in {student.course_name}.')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list[Student]) -> list[Student]:
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            student = Student(student_first_name,
                              student_last_name,
                              course_name)
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the incorrect type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# ╚══ END CLASS SECTION ══════════════════════════════╝

# Define the Data Variables
students: list[Student] = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

# ╔══ MAIN CONTENT ═══════════════════════════════════╗

# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print(EXIT_MSG)
