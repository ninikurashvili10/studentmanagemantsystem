import time
import json
import os

# შევქმნათ სტუდენტის კლასი
class Student:
    def __init__(self, name: str, roll_num: int, grade: chr):
        self.name = name
        self.roll_num = roll_num
        self.grade = grade

    # ქულის განახლების ფუნქციონალი
    def update_grade(self, new_grade):
        self.grade = new_grade
    #ობიექტის ინფორმაციის დიქშენარად გადაქცევა
    def to_dict(self):
        return {"name": self.name, "roll_num": self.roll_num, "grade": self.grade}
    #დიქშენარიდან კლასის ტიპად გადაქცევა ინფორმაციის
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["roll_num"], data["grade"])
    # დაპრინტვისას სტუდენტის ობიექტის ინფორმაციის გამოსატანად
    def __repr__(self):
        return f'{{"name": "{self.name}", "roll_num": {self.roll_num}, "grade": "{self.grade}"}}'


class StudentManagementSystem:
    # მოვახდინოთ სტუდენტების მართვის სისტემის ინიციალიზება ცარიელი სტუდენტების ლისტით,ჩარიცხვის რიცხვით,json ფაილის შექმნით, ან უკვე შექმნილი ფაილიდან ინფორმაციის გადმოწერით
    def __init__(self):
        self.students = []
        self.current_roll_num = 1
        self.initialize_json_file()
        self.load_students()

    # ცარიელიjson ფაილის შექმნა თუ უკვე შექმნილი არ არის
    def initialize_json_file(self):
        if not os.path.exists("students.json"):
            with open("students.json", 'w') as file:
                json.dump([], file)

    # ინფორმაციის გადმოტანა ფაილიდან
    def load_students(self):
        with open("students.json", 'r') as file:
            student_data = json.load(file)
            self.students = [Student.from_dict(data) for data in student_data]
            if self.students:
                self.current_roll_num = max(student.roll_num for student in self.students) + 1

    # ფაილში ინფორმაციის ჩაწერა
    def save_students(self):
        with open("students.json", 'w') as file:
            json.dump([student.to_dict() for student in self.students], file,indent=4)

    # ქულის ვალიდაციის ფუნქცია,რომელიც ითვალისწინებს რომ შეყვანილი შეფასება იქნება (A-F) ის ტიპის
    def validate_grade(self):
        grade = input("Enter Grade (A-F): ").strip().upper()
        while grade not in ['A', 'B', 'C', 'D', 'E', 'F']:
            grade = input("Invalid Grade. Enter a grade (A-F): ").strip().upper()
        return grade

    # სახელის ვალიდაციის ფუნქცია,რომელიც ითვალისწინებს რომ შეყვანილი სახელი შეიცავს მხოლოდ ანბანის ასოებს
    def validate_name(self):
        while True:
            name = input("Enter Student's Name: ").strip().title()
            if name.isalpha():
                return name
            else:
                print("Invalid name. Please enter a name containing only alphabetic characters.")

    # სტუდენტის ფუნქციის დამატების მეთოდი
    def add_student(self):
        name = self.validate_name()
        grade = self.validate_grade()
        roll_num = self.current_roll_num
        student = Student(name, roll_num, grade)
        self.students.append(student)
        self.save_students()
        self.current_roll_num += 1
        print("Student added successfully")

    # ყველა სტუდენტის ნახვის მეთოდი
    def view_students(self):
        if not self.students:
            print("There are no students")
        else:
            print("Students list:")
            for i, student in enumerate(self.students, 1):
                print(f"{i}. {student}")

    # ყველა სტუდენტის წაშლა
    def delete_all_students(self):
        confirm = input("Are you sure you want to delete all student data? (Yes/No): ").strip().lower()
        if confirm == "yes":
            self.students.clear()
            self.save_students()
            print("All students have been deleted.")
        else:
            print("Operation canceled.")

    # სტუდენტის მოძებნა roll_num-ით
    def search_student_by_roll_num(self):
        while True:
            try:
                roll_num = int(input("Enter Roll Number: ").strip())
                if roll_num <= 0:
                    print("Roll Number must be greater than 0. Please try again.")
                else:
                    break
            except ValueError:
                print("Invalid Roll Number. Please enter an integer.")
        for student in self.students:
            if student.roll_num == roll_num:
                while True:
                    print(f"Student found:{student}")
                    print("choose an action")
                    print("\t1. Update student grade")
                    print("\t2. Remove student")
                    print("\t3. Exit")
                    choice = input("Enter your choice's number: ")
                    if choice == "1":
                        self.update_student_grade(student)
                    elif choice == "2":
                        self.remove_student(student)
                        break
                    elif choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")
                break
        else:
            print("No student found with that roll number.")

    # სტუდენტის ქულის განახლება,რომელიც გამოიყენება სტუდენტის მოძებნის შემდეგ ,არგუმენტს გადასცემს search_student_by_roll_num მეთოდი
    def update_student_grade(self, student):
        new_grade = self.validate_grade()
        student.update_grade(new_grade)
        self.save_students()
        print("Student's grade updated successfully.")

    # სტუდენტის წაშლის მეთოდი,რომელიც გამოიყენება სტუდენტის მოძებნის შემდეგ ,არგუმენტს გადასცემს search_student_by_roll_num მეთოდი
    def remove_student(self, student):
        self.students.remove(student)
        self.save_students()
        print(f"Student has been removed successfully.")

    # მენიუ, რომლითაც მომხმარებელი ირჩევს შესაბამის მოქმედებას
    def menu(self):
        while True:
            print("-------------------------")
            print("Student Management System \nChoose an operation:")
            print("\t1. Add a new student")
            print("\t2. View all students")
            print("\t3. Search student by roll num (then modify)")
            print("\t4. Delete all data")
            print("\t5. Exit")
            print("-------------------------")

            choice = input("Enter your choice's number: ")
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student_by_roll_num()
            elif choice == "4":
                self.delete_all_students()
                time.sleep(1)
                continue
            elif choice == "5":
                print("Thank you for using Student Management System.\nExiting...")
                break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                continue
            if not self.exit_or_continue():
                break

    # გვთავაზობს გვინდა თუ არა გაგრძელება
    def exit_or_continue(self):
        while True:
            choice = input("Do you want to continue? (Yes/No): ").strip().lower()
            if choice == "no":
                print("Thank you for using the Student Management System.\nExiting...")
                return False
            elif choice == "yes":
                return True
            else:
                print("Invalid choice. Please try again")


# სტუდენტების მართვის სისტემის ობიექტის შექმნა
students_system = StudentManagementSystem()
# მენიუს გამოძახება
students_system.menu()





