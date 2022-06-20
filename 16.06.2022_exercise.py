class SchoolMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        self.classes_thought = []
        self.salary = salary
        super().__init__(name, age)

    def add_class(self, new_class):
        self.classes_thought.append(new_class)


class Student(SchoolMember):
    def __init__(self, name, age, classes_enrolled, year_enrolled, grades):
        self.classes_enrolled = []
        self.year_enrolled = {}
        self.grades = {}
        super().__init__(name, age)

    def enroll_class(self, new_enrolled_class):
        self.classes_enrolled.append(new_enrolled_class)

    def class_year(self, class_name, year_enrolled):
        self.year_enrolled[year_enrolled] = class_name

    def grade(self, grade_received, class_attended):
        self.grades[class_attended] = grade_received