from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QSpacerItem, QSizePolicy
)

class MainMenu(QWidget):
    def __init__(self, switch_to_mode_callback):
        super().__init__()

        self.language_options = ("PL", "EN", "MIX")
        self.current_lang_index = 0

        self.lang_label = QLabel("Language:")
        self.lang_button = QPushButton(self.language_options[self.current_lang_index])
        self.lang_button.clicked.connect(self.cycle_language)

        lang_layout = QHBoxLayout()
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_button)

        self.mode_label = QLabel("Mode:")
        self.mode1_button = QPushButton("Name → Codes + Structure")


        self.mode1_button.clicked.connect(
            lambda: switch_to_mode_callback(self.language_options[self.current_lang_index])
        )

        inner_layout = QVBoxLayout()
        inner_layout.addLayout(lang_layout)
        inner_layout.addSpacing(20)
        inner_layout.addWidget(self.mode_label)
        inner_layout.addWidget(self.mode1_button)

        inner_container = QWidget()
        inner_container.setLayout(inner_layout)

        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(inner_container)
        center_row.addStretch()
        outer_layout.addLayout(center_row)
        outer_layout.addStretch()

        self.setLayout(outer_layout)
        self.resize(400, 300)

    def cycle_language(self):
        self.current_lang_index = (self.current_lang_index + 1) % len(self.language_options)
        self.lang_button.setText(self.language_options[self.current_lang_index])
