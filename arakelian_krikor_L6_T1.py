class SchoolMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        self.classes_taught = {}
        self.salary = salary
        super().__init__(name, age)

    def getSalary(self):
        return self.salary

    def addCourse(self, signature, name):
        self.classes_taught[signature] = name

    def getCourses(self):
        for signature, name in self.classes_taught.items():
            print(f"{signature} {name}")


class Student(SchoolMember):
    def __init__(self, name, age):
        self.courses = {}
        super().__init__(name, age)

    def attendCourse(self, signature, year):
        self.courses.setdefault(signature, {'grades': []})
        self.courses[signature]['year'] = year

    def addGrade(self, signature, grade):
        if signature in self.courses:
            self.courses[signature]['grades'].append(grade)

    def getCourses(self):
        for signature in self.courses:
            print(f"{signature} {self.courses[signature]}")

    def getAvgGrade(self, signature):
        return f"{sum(self.courses[signature]['grades']) / len(self.courses[signature]['grades']):.1f}"
