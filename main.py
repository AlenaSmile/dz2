import sys
from front import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database


db = Database()


class AddTeacherForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddTeacherForm, self).__init__(parent)
        self.setWindowTitle("Добавить Учителя")
        self.setGeometry(100, 100, 300, 400)
        self.last_name_label = QtWidgets.QLabel("Фамилия:", self)
        self.last_name_label.setGeometry(10, 10, 100, 30)
        self.last_name_input = QtWidgets.QLineEdit(self)
        self.last_name_input.setGeometry(120, 10, 150, 30)
        self.first_name_label = QtWidgets.QLabel("Имя:", self)
        self.first_name_label.setGeometry(10, 50, 100, 30)
        self.first_name_input = QtWidgets.QLineEdit(self)
        self.first_name_input.setGeometry(120, 50, 150, 30)
        self.middle_name_label = QtWidgets.QLabel("Отчество:", self)
        self.middle_name_label.setGeometry(10, 90, 100, 30)
        self.middle_name_input = QtWidgets.QLineEdit(self)
        self.middle_name_input.setGeometry(120, 90, 150, 30)
        self.phone_label = QtWidgets.QLabel("Телефон:", self)
        self.phone_label.setGeometry(10, 130, 100, 30)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.phone_input.setGeometry(120, 130, 150, 30)
        self.email_label = QtWidgets.QLabel("Емейл:", self)
        self.email_label.setGeometry(10, 170, 100, 30)
        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setGeometry(120, 170, 150, 30)
        self.comment_label = QtWidgets.QLabel("Комментарий:", self)
        self.comment_label.setGeometry(10, 210, 100, 30)
        self.comment_input = QtWidgets.QLineEdit(self)
        self.comment_input.setGeometry(120, 210, 150, 30)
        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setGeometry(100, 300, 100, 30)
        self.add_button.clicked.connect(self.add_teacher)

    def add_teacher(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        middle_name = self.middle_name_input.text()
        if not any ((last_name, first_name, middle_name)):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Поля ФИО обязательны для заполнения!")
            return
        phone = self.phone_input.text()
        email = self.email_input.text()
        comment = self.comment_input.text()
        fio = f"{last_name} {first_name} {middle_name}"
        self.accept()
        try:
            db.add_teacher(fio, phone, email, comment)
            QtWidgets.QMessageBox.information(self, "Успех", "Учитель успешно добавлен!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))

    def accept(self):
        super(AddTeacherForm, self).accept()


class AddStudentForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddStudentForm, self).__init__(parent)
        self.setWindowTitle("Добавить ученика")
        self.setGeometry(100, 100, 300, 400)
        self.last_name_label = QtWidgets.QLabel("Фамилия:", self)
        self.last_name_label.setGeometry(10, 10, 100, 30)
        self.last_name_input = QtWidgets.QLineEdit(self)
        self.last_name_input.setGeometry(120, 10, 150, 30)
        self.first_name_label = QtWidgets.QLabel("Имя:", self)
        self.first_name_label.setGeometry(10, 50, 100, 30)
        self.first_name_input = QtWidgets.QLineEdit(self)
        self.first_name_input.setGeometry(120, 50, 150, 30)
        self.middle_name_label = QtWidgets.QLabel("Отчество:", self)
        self.middle_name_label.setGeometry(10, 90, 100, 30)
        self.middle_name_input = QtWidgets.QLineEdit(self)
        self.middle_name_input.setGeometry(120, 90, 150, 30)
        self.group_label = QtWidgets.QLabel("Группа:", self)
        self.group_label.setGeometry(10, 130, 100, 30)
        self.group_input = QtWidgets.QComboBox(self)
        groups = db.get_all_groups()
        self.group_input.setGeometry(120, 130, 150, 30)
        self.group_input.addItems(groups)
        self.group_input.setEditable(True)
        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setGeometry(100, 300, 100, 30)
        self.add_button.clicked.connect(self.add_student)

    def add_student(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        middle_name = self.middle_name_input.text()
        group = self.group_input.currentText()
        if not any((last_name, first_name, middle_name)):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Поля ФИО обязательны для заполнения!")
            return
        fio = f"{last_name} {first_name} {middle_name}"
        self.accept()
        try:
            db.add_student(fio, group)
            QtWidgets.QMessageBox.information(self, "Успех", "Ученик успешно добавлен!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))

    def accept(self):
        super(AddStudentForm, self).accept()


class AddTaskForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddTaskForm, self).__init__(parent)
        self.setWindowTitle("Добавить вопрос")
        self.setGeometry(100, 100, 300, 400)
        self.question_label = QtWidgets.QLabel("Вопрос:", self)
        self.question_label.setGeometry(10, 10, 100, 30)
        self.question_input = QtWidgets.QLineEdit(self)
        self.question_input.setGeometry(120, 10, 150, 30)
        self.content_label = QtWidgets.QLabel("Доп. информация", self)
        self.content_label.setGeometry(10, 50, 110, 30)
        self.content_input = QtWidgets.QTextEdit(self)
        self.content_input.setGeometry(120, 50, 150, 100)
        self.content_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setGeometry(100, 300, 100, 30)
        self.add_button.clicked.connect(self.add_task)

    def accept(self):
        super(AddTaskForm, self).accept()

    def add_task(self):
        question = self.question_input.text()
        content = self.content_input.toPlainText()
        self.accept()
        try:
            db.add_question(question, content)
            QtWidgets.QMessageBox.information(self, "Успех", "Вопрос успешно добавлен!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))


class TestSetupForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TestSetupForm, self).__init__(parent)
        self.all_questions = db.get_all_questions()
        self.all_teachers = db.get_all_teachers()
        teacher_names = [t['fio'] for t in self.all_teachers]
        self.setWindowTitle("Настройка теста")
        self.setGeometry(100, 100, 400, 500)
        self.teacher_label = QtWidgets.QLabel("Выберите учителя:", self)
        self.teacher_label.setGeometry(10, 10, 120, 30)
        self.teacher_combo = QtWidgets.QComboBox(self)
        self.teacher_combo.setGeometry(150, 10, 200, 30)
        self.teacher_combo.addItems(teacher_names)
        self.test_name_label = QtWidgets.QLabel("Название теста:", self)
        self.test_name_label.setGeometry(10, 50, 120, 30)
        self.test_name_input = QtWidgets.QLineEdit(self)
        self.test_name_input.setGeometry(150, 50, 200, 30)
        self.question_count_label = QtWidgets.QLabel("Количество вопросов:", self)
        self.question_count_label.setGeometry(10, 90, 120, 30)
        self.question_count_input = QtWidgets.QSpinBox(self)
        self.question_count_input.setGeometry(150, 90, 100, 30)
        self.question_count_input.setMinimum(1)
        self.set_button = QtWidgets.QPushButton("Установить", self)
        self.set_button.setGeometry(10, 130, 100, 30)
        self.set_button.clicked.connect(self.setup_questions)
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setGeometry(10, 170, 360, 260)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.create_button = QtWidgets.QPushButton("Создать", self)
        self.create_button.setGeometry(150, 440, 100, 30)
        self.create_button.clicked.connect(self.create_test)
        self.create_button.setVisible(False)

    def setup_questions(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        count = self.question_count_input.value()
        if count > len(self.all_questions):
            count = len(self.all_questions)
            QtWidgets.QMessageBox.warning(self, "Внимание", "Количество вопросов больше количества вопросов в базе!\n"
                                                              "Установлено количество вопросов: " + str(count))
        for i in range(count):
            question_label = QtWidgets.QLabel(f"Вопрос {i + 1}:", self.scroll_widget)
            self.layout.addWidget(question_label)
            question_combo = QtWidgets.QComboBox(self.scroll_widget)
            question_combo.addItems(self.all_questions)
            self.layout.addWidget(question_combo)
        self.create_button.setVisible(True)

    def create_test(self):
        test_name = self.test_name_input.text()
        if not test_name:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Название теста не может быть пустым!")
            return
        selected_teacher = self.teacher_combo.currentText()
        teacher_id = self.all_teachers[[t['fio'] for t in self.all_teachers].index(selected_teacher)]['teacher_id']
        questions = [self.layout.itemAt(i).widget().currentText() for i in range(self.layout.count()) if
                     isinstance(self.layout.itemAt(i).widget(), QtWidgets.QComboBox)]
        questions_ids = [db.get_question_id(q) for q in questions]
        variant_id = db.add_variant(test_name, teacher_id)
        for q_id in questions_ids:
            db.add_variant_test(variant_id, q_id)
        QtWidgets.QMessageBox.information(self, "Создание теста", "Тест создан!")


class SetTaskForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SetTaskForm, self).__init__(parent)
        self.all_students = db.get_all_students()
        self.all_groups = db.get_all_groups()
        self.all_groups = [''] + self.all_groups
        students_names = [s['fio'] for s in self.all_students]
        students_names = [''] + students_names
        self.all_variants = db.get_all_variants()
        variants_titles = [s['title'] for s in self.all_variants]
        variants_titles = [''] + variants_titles
        self.setWindowTitle("Назначить тест")
        self.setGeometry(100, 100, 300, 300)
        self.student_label = QtWidgets.QLabel("Учащийся:", self)
        self.student_label.setGeometry(10, 10, 100, 30)
        self.student_combo = QtWidgets.QComboBox(self)
        self.student_combo.setGeometry(120, 10, 150, 30)
        self.student_combo.addItems(students_names)
        self.test_label = QtWidgets.QLabel("Тест:", self)
        self.test_label.setGeometry(10, 50, 100, 30)
        self.test_combo = QtWidgets.QComboBox(self)
        self.test_combo.setGeometry(120, 50, 150, 30)
        self.test_combo.addItems(variants_titles)
        self.group_label = QtWidgets.QLabel("Группа:", self)
        self.group_label.setGeometry(10, 90, 100, 30)
        self.group_combo = QtWidgets.QComboBox(self)
        self.group_combo.setGeometry(120, 90, 150, 30)
        self.group_combo.addItems(self.all_groups)
        self.tooltip_label = QtWidgets.QLabel("?", self)
        self.tooltip_label.setGeometry(280, 90, 20, 20)
        self.tooltip_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tooltip_label.setToolTip("Если выбрать конкретную группу, то тест будет"
                                      " назначен всем учащимся этой группы.")
        self.tooltip_label.setStyleSheet("background-color: lightgray; border-radius: 10px;")
        self.assign_button = QtWidgets.QPushButton("Назначить", self)
        self.assign_button.setGeometry(100, 130, 100, 30)
        self.assign_button.clicked.connect(self.assign_task)

    def accept(self):
        super(SetTaskForm, self).accept()

    def assign_task(self):
        student = self.student_combo.currentText()
        test = self.test_combo.currentText()
        group = self.group_combo.currentText()
        if not test:
            QtWidgets.QMessageBox.warning(self, "Внимание", "Тест не выбран!")
            return
        elif not any([student, group]):
            QtWidgets.QMessageBox.warning(self, "Внимание", "Вы должны выбрать учащегося или группу!")
            return
        self.accept()
        try:
            if group:
                test_id = self.all_variants[[s['title'] for s in self.all_variants].index(test)]['variant_id']
                db.assign_variant_by_group(group, test_id)
            else:
                student_id = self.all_students[[s['fio'] for s in self.all_students].index(student)]['student_id']
                test_id = self.all_variants[[s['title'] for s in self.all_variants].index(test)]['variant_id']
                db.assign_variant_by_student(student_id, test_id)
            QtWidgets.QMessageBox.information(self, "Успех", "Задание успешно назначено!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_teacher_btn.clicked.connect(self.add_teacher)
        self.add_student_btn.clicked.connect(self.add_student)
        self.add_qstn_btn.clicked.connect(self.add_task)
        self.add_test_btn.clicked.connect(self.add_test)
        self.set_test_btn.clicked.connect(self.set_test)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_teacher(self):
        self.hide()
        self.add_teacher_form = AddTeacherForm(self)
        if self.add_teacher_form.exec_() == QtWidgets.QDialog.Accepted:
            pass
        self.show()

    def add_student(self):
        self.hide()
        self.add_student_form = AddStudentForm(self)
        if self.add_student_form.exec_() == QtWidgets.QDialog.Accepted:
            pass
        self.show()

    def add_task(self):
        self.hide()
        self.add_task_form = AddTaskForm(self)
        if self.add_task_form.exec_() == QtWidgets.QDialog.Accepted:
            pass
        self.show()

    def add_test(self):
        self.hide()
        self.test_creator = TestSetupForm(self)
        if self.test_creator.exec_() == QtWidgets.QDialog.Accepted:
            pass
        self.show()

    def set_test(self):
        self.hide()
        self.set_test_form = SetTaskForm(self)
        if self.set_test_form.exec_() == QtWidgets.QDialog.Accepted:
            pass
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())