import os
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QLineEdit
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from database import amino_acids
from random import sample, choice, shuffle

def grade_quiz(quiz_data):
    score = 0
    total = len(quiz_data)

    for entry in quiz_data:
        correct_id = entry["id"]
        correct_three = amino_acids[correct_id]["3_letter"]
        correct_structure = amino_acids[correct_id]["structure"]

        is_correct = (
            entry["1-l-code"].strip().upper() == correct_id and
            entry["3-l-code"].strip().capitalize() == correct_three and
            entry["img-selected"] == correct_structure
        )

        if is_correct:
            score += 1

    return score, total

class NameToCodeModeSetup(QWidget):
    def __init__(self, back_callback, start_quiz_callback, lang):
        super().__init__()

        self.available_options = ['A', 'R', 'N', 'D', 'C',
                                 'E', 'Q', 'G', 'H', 'I',
                                 'L', 'K', 'M', 'F', 'P',
                                 'S', 'T', 'W', 'Y', 'V']
        self.start_quiz_callback = start_quiz_callback
        self.lang = lang.lower()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Choose cathegory:"))

        categories = {
            "Sprint (5)": 5,
            "Mile (10)": 10,
            "Medium (15)": 15,
            "Long (20)": 20
        }

        for label, count in categories.items():
            button = QPushButton(label)
            button.clicked.connect(lambda _, c=count: self.pick_random(c))
            layout.addWidget(button)

        back_button = QPushButton("Back to menu")
        back_button.clicked.connect(back_callback)

        layout.addSpacing(60)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def pick_random(self, count):
        selected = sample(self.available_options, count)

        lang_opt = ("en", "pl")

        quiz_data = []
        for acid in selected:
            if self.lang in lang_opt:
                name = amino_acids[acid][self.lang]
            else:
                name = amino_acids[acid][choice(lang_opt)]

        correct_structure = amino_acids[acid]["structure"]

        other_acids = [a for a in self.available_options if a != acid]
        fake_acids = sample(other_acids, 3)
        fake_structures = [amino_acids[f]["structure"] for f in fake_acids]

        all_structures = fake_structures + [correct_structure]
        shuffle(all_structures)

        for acid in selected:
            if (self.lang in lang_opt):
                name = amino_acids[acid][self.lang]
            else:
                name = amino_acids[acid][choice(lang_opt)]
            quiz_data.append({
                "id": acid,
                "name": name,
                "1-l-code": "",
                "3-l-code": "",
                "imgs": all_structures,
                "img-selected": None
            })
        self.start_quiz_callback(quiz_data)

class NameToCodeMode(QWidget):
    def __init__(self, back_callback, quiz_data):
        super().__init__()

        self.quiz_data = quiz_data
        self.current_index = 0

        layout = QVBoxLayout()
        self.counter_label = QLabel()
        layout.addWidget(self.counter_label)

        self.name_label = QLabel()
        layout.addWidget(self.name_label)

        self.one_letter_label = QLabel("1 Letter Abbreviation:")
        self.one_letter_input = QLineEdit()
        self.one_letter_input.setMaxLength(1)
        layout.addWidget(self.one_letter_label)
        layout.addWidget(self.one_letter_input)

        self.three_letter_label = QLabel("3 Letter Abbreviation:")
        self.three_letter_input = QLineEdit()
        self.three_letter_input.setMaxLength(3)
        layout.addWidget(self.three_letter_label)
        layout.addWidget(self.three_letter_input)

        self.image_buttons = []
        img_layout = QHBoxLayout()
        for i in range(4):
            btn = QPushButton()
            btn.clicked.connect(lambda _, idx=i: self.select_image(idx))
            self.image_buttons.append(btn)
            img_layout.addWidget(btn)
        layout.addLayout(img_layout)

        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("<<")
        self.prev_button.clicked.connect(self.go_prev)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton(">>")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        back_button = QPushButton("Back to menu")
        back_button.clicked.connect(back_callback)
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.update_display()

    def update_display(self):
        total = len(self.quiz_data)
        self.counter_label.setText(f"Amino Acid {self.current_index + 1}/{total}")
        current_item = self.quiz_data[self.current_index]
        self.name_label.setText(current_item["name"])

        for btn, img_file in zip(self.image_buttons, current_item["imgs"]):
            path = os.path.join("structures", img_file)
            btn.setIconSize(btn.size())
            btn.setIcon(QIcon(path))

        self.one_letter_input.blockSignals(True)
        self.three_letter_input.blockSignals(True)
        self.one_letter_input.setText(current_item["1-l-code"])
        self.three_letter_input.setText(current_item["3-l-code"])
        self.one_letter_input.blockSignals(False)
        self.three_letter_input.blockSignals(False)

        self.prev_button.setVisible(self.current_index > 0)
        self.next_button.setText("Submit" if self.current_index == total - 1 else ">>")

    def select_image(self, index):
        selected_img = self.quiz_data[self.current_index]["imgs"][index]
        self.quiz_data[self.current_index]["img-selected"] = selected_img

    def go_prev(self):
        self.save_current_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

    def go_next(self):
        self.save_current_answer()
        if self.current_index < len(self.quiz_data) - 1:
            self.current_index += 1
            self.update_display()
        else:
            score, total = grade_quiz(self.quiz_data)
            self.parent().setCentralWidget(QuizResultScreen(score, total, self.parent().back_to_menu))

    def save_current_answer(self):
        self.quiz_data[self.current_index]["1-l-code"] = self.one_letter_input.text()
        self.quiz_data[self.current_index]["3-l-code"] = self.three_letter_input.text()

class QuizResultScreen(QWidget):
    def __init__(self, score, total, back_callback):
        super().__init__()

        layout = QVBoxLayout()

        layout.addStretch()
        label = QLabel(f"Quiz Finished!\nScore: {score}/{total}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addStretch()

        back_button = QPushButton("Back to Menu")
        back_button.clicked.connect(back_callback)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

