import time


# შევქმნათ სტუდენტის კლასი
class Student:
    def __init__(self, name: str, roll_num: int, grade: chr):
        self.name = name
        self.roll_num = roll_num
        self.grade = grade

    # ქულის განახლების ფუნქციონალი
    def update_grade(self, new_grade):
        self.grade = new_grade

    # დაპრინტვისას სტუდენტის ობიექტის ინფორმაციის გამოსატანად
    def __repr__(self):
        return f'{{"name": "{self.name}", "roll_num": {self.roll_num}, "grade": "{self.grade}"}}'


class StudentManagementSystem:
    # მოვახდინოთ სტუდენტების მართვის სისტემის ინიციალიზება ცარიელი სტუდენტების ლისტით
    def __init__(self):
        self.students = []

    # roll_number-ის ვალიდაციის ფუნქცია,რომელიც ითვალისწინებს რომ ის იყოს ინტეჯერი და ნატურალური რიცხვი
    def validate_roll_num(self):
        while True:
            try:
                roll_num = int(input("Enter Roll Number: ").strip())
                if roll_num <= 0:
                    print("Roll Number must be greater than 0. Please try again.")
                else:
                    return roll_num
            except ValueError:
                print("Invalid Roll Number.Please enter an integer")

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

    # სტუდენტის ფუნქციის დამატების მეთოდი,რომელიც ითვალისწინებს რომ ერთი და იგივე roll number-ით არ მოხდეს დამატება
    def add_student(self):
        name = self.validate_name()
        roll_num = self.validate_roll_num()
        while roll_num in {student.roll_num for student in self.students}:
            print("This roll number already exists. Please enter a unique roll number.")
            roll_num = self.validate_roll_num()
        grade = self.validate_grade()
        student = Student(name, roll_num, grade)
        self.students.append(student)
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
            print("All students have been deleted.")
        else:
            print("Operation canceled.")

    # სტუდენტის მოძებნა roll_num-ით
    def search_student_by_roll_num(self):
        roll_num = self.validate_roll_num()
        for student in self.students:
            if student.roll_num == roll_num:
                while True:
                    print(f"Student found:{student}")
                    print("choose an action")
                    print("\t1. Update student grade")
                    print("\t2. remove a student")
                    print("\t3. exit")
                    choice = input("Enter your choice's number: ")
                    if choice == "1":
                        self.update_student_grade(student)
                    elif choice == "2":
                        self.remove_student(student)
                        break
                    elif choice == "3":
                        break
                    else:
                        print("invalid choice. Please try again.")
                break
        else:
            print("No student found with that roll number.")


    # სტუდენტის ქულის განახლება,რომელიც გამოიყენება სტუდენტის მოძებნის შემდეგ ,არგუმენტს გადასცემს search_student_by_roll_num მეთოდი
    def update_student_grade(self,student):
        if student:
            new_grade = self.validate_grade()
            student.update_grade(new_grade)
            print("Student's grade updated successfully.")

    # სტუდენტის წაშლის მეთოდი,რომელიც გამოიყენება სტუდენტის მოძებნის შემდეგ ,არგუმენტს გადასცემს search_student_by_roll_num მეთოდი
    def remove_student(self, student):
        if student:
            self.students.remove(student)
            print(f"Student has been removed successfully.")


    # მენიუ, რომლითაც მომხმარებელი ირჩევს შესაბამის მოქმედებას
    def menu(self):
        while True:
            print("-------------------------")
            print("Student Management System \nchoose an operation:")
            print("\t1. Add a new student")
            print("\t2. View all students")
            print("\t3. Search student by roll num(then modifying)")
            print("\t4. delete all data")
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
                print("Invalid choice. Please try again")
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






