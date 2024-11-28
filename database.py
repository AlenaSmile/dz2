import sqlite3
from sqlite3 import IntegrityError

class Database:
    def __init__(self, path: str = 'db.db'):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        sql = """create table if not exists teachers (
                    id_teacher integer primary key not null,
                    fio varchar(500) not null unique,
                    phone char(10) null,
                    email varchar(255) null,
                    comnt text null
                );
                create table if not exists variants (
                    id_variant integer primary key not null,
                    title varchar(200) not null,
                    vcreated timestamp default current_timestamp,
                    teacher_id integer not null references teachers(id_teacher)
                );
                create table if not exists tests (
                    id_test integer primary key not null,
                    tname varchar(200) null unique,
                    tcontent text not null,
                    teacher_id integer null references teachers(id_teacher)
                );
                create table if not exists variants_tests (
                    variant_id integer not null references variants(id_variant),
                    test_id integer not null references tests(id_test),
                    unique(variant_id, test_id)
                );
                create table if not exists students (
                    id_student integer primary key not null,
                    fio varchar(500) not null unique,
                    student_group char(10) null
                );
                create table if not exists students_tests (
                    student_id integer not null references students(id_student),
                    test_id integer not null references tests(id_test),
                    unique(student_id, test_id)
                );
        """
        self.cursor.executescript(sql)
        self.conn.commit()

    def add_teacher(self, fio: str, phone: str = '', email: str = '', comment: str = ''):
        try:
            self.cursor.execute("INSERT INTO teachers (fio, phone, email, comnt) VALUES (?, ?, ?, ?)",
                                (fio, phone, email, comment))
            self.conn.commit()
        except IntegrityError:
            self.conn.rollback()
            raise ValueError('Такой учитель уже существует')

    def add_student(self, fio: str, group: str):
        try:
            self.cursor.execute("INSERT INTO students (fio, student_group) VALUES (?, ?)", (fio, group))
            self.conn.commit()
        except IntegrityError:
            self.conn.rollback()
            raise ValueError('Такой ученик уже существует')

    def add_question(self, title: str, content: str):
        try:
            self.cursor.execute("INSERT INTO tests (tname, tcontent) VALUES (?, ?)", (title, content))
            self.conn.commit()
        except IntegrityError:
            self.conn.rollback()
            raise ValueError('Задача с таким названием уже существует')

    def get_all_groups(self) -> list[str]:
        self.cursor.execute("SELECT DISTINCT student_group FROM students")
        return [i[0] for i in self.cursor.fetchall()]

    def get_all_questions(self) -> list[str]:
        self.cursor.execute("SELECT tname FROM tests")
        return [i[0] for i in self.cursor.fetchall()]

    def get_all_teachers(self) -> list[dict]:
        result = []
        self.cursor.execute("SELECT id_teacher, fio FROM teachers")
        data = self.cursor.fetchall()
        for i in data:
            result.append({'teacher_id': i[0], 'fio': i[1]})
        return result

    def get_question_id(self, title: str) -> int:
        self.cursor.execute("SELECT id_test FROM tests WHERE tname = ?", (title,))
        return self.cursor.fetchone()[0]

    def get_all_students(self) -> list[dict]:
        result = []
        self.cursor.execute("SELECT id_student, fio FROM students")
        data = self.cursor.fetchall()
        for i in data:
            result.append({'student_id': i[0], 'fio': i[1]})
        return result

    def get_all_variants(self) -> list[dict]:
        result = []
        self.cursor.execute("SELECT id_variant, title FROM variants")
        data = self.cursor.fetchall()
        for i in data:
            result.append({'variant_id': i[0], 'title': i[1]})
        return result

    def get_students_by_group(self, group: str) -> list[int]:
        self.cursor.execute("SELECT id_student FROM students WHERE student_group = ?", (group,))
        return [i[0] for i in self.cursor.fetchall()]

    def add_variant(self, title: str, teacher_id: int) -> int:
        self.cursor.execute("INSERT INTO variants (title, teacher_id) VALUES (?, ?) RETURNING id_variant",
                            (title, teacher_id))
        id_variant = self.cursor.fetchone()[0]
        self.conn.commit()
        return id_variant

    def add_variant_test(self, variant_id: int, test_id: int):
        self.cursor.execute("INSERT INTO variants_tests (variant_id, test_id) VALUES (?, ?)",
                            (variant_id, test_id))
        self.conn.commit()

    def assign_variant_by_group(self, group: str, variant_id: int):
        students_ids = self.get_students_by_group(group)
        for s_id in students_ids:
            try:
                self.cursor.execute("INSERT INTO students_tests (student_id, test_id) VALUES (?, ?)",
                                    (s_id, variant_id))
                self.conn.commit()
            except IntegrityError:
                self.conn.rollback()

    def assign_variant_by_student(self, student_id: int, variant_id: int):
        try:
            self.cursor.execute("INSERT INTO students_tests (student_id, test_id) VALUES (?, ?)",
                                (student_id, variant_id))
            self.conn.commit()
        except IntegrityError:
            self.conn.rollback()
            raise ValueError('Этому ученику уже назначен этот тест.')
