
from src.configuration.config import WINDOW_HEIGHT, WINDOW_WIDTH, SCROLL_HEIGHT, SCROLL_WIDTH, BUTTON_WIDTH, \
    BUTTON_HEIGHT, LINE_EDIT_SIZE, APP_BG_COLOR
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
    QFrame
)


class LiuWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""
    # tasks_list = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.general_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setStyleSheet(f"background-color: {APP_BG_COLOR}")
        central_widget.setLayout(self.general_layout)
        self.setCentralWidget(central_widget)

        self._set_user_quarter()
        self._set_input_quarter()
        self._set_output_quarter()
        self._set_graph_quarter()

    def _set_user_quarter(self):
        # user input
        self.user_min_time = QLineEdit()
        self.user_max_time = QLineEdit()
        self.user_tasks_number = QLineEdit()
        self.user_min_time.setFixedWidth(LINE_EDIT_SIZE)
        self.user_max_time.setFixedWidth(LINE_EDIT_SIZE)
        self.user_tasks_number.setFixedWidth(LINE_EDIT_SIZE)

        # layout for user's input
        user_input_layout = QFormLayout()
        user_input_layout.addRow("<p style=\"font-size:15px\">Minimum time:</p>", self.user_min_time)
        user_input_layout.addRow("<p style=\"font-size:15px\">Maximum time:</p>", self.user_max_time)
        user_input_layout.addRow("<p style=\"font-size:15px\">Tasks number:</p>", self.user_tasks_number)
        user_input_widget = QWidget()
        user_input_widget.setLayout(user_input_layout)

        # buttons
        self.button_clear = QPushButton("Clear all")
        self.button_user = QPushButton("Create tasks")
        self.button_default = QPushButton("Create default tasks")
        self.button_run_alg = QPushButton("Order tasks")

        self.button_clear.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_user.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_default.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_run_alg.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.button_clear.setStyleSheet(
            "font-size:15px; font-weight:bold; border-radius : 5; background-color: #DE3163; color:white; border-bottom: 1px solid grey; border-right:1px solid grey;")
        self.button_user.setStyleSheet(
            "font-size:15px; border-radius : 5; background-color: #cfeafb; color:black; border-bottom: 1px solid grey; border-right:1px solid grey;")
        self.button_default.setStyleSheet(
            "font-size:15px; border-radius : 5; background-color: #cfeafb; color:black; border-bottom: 1px solid grey; border-right:1px solid grey;")
        self.button_run_alg.setStyleSheet(
            "font-size:15px; border-radius : 5; background-color: #cfeafb; color:black; border-bottom: 1px solid grey; border-right:1px solid grey;")

        # invalid params label
        self.invalid_params_label = QLabel("")
        self.invalid_params_label.setStyleSheet("font-size:15px; color:red")

        # add user input layout to user quarter layout
        self.user_quarter_layout = QVBoxLayout()
        self.user_quarter_layout.addWidget(QLabel("<h1>Algorithm Liu</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(QLabel("<h2>1 | r<sub>i</sub>, prm | L<sub>max</sub></h2>"),
                                           alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(user_input_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_user, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_default, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_run_alg, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_clear, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.invalid_params_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # add user's layout to user widget
        self.general_layout.addLayout(self.user_quarter_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    def _set_input_quarter(self):
        # input values layout
        self.input_values_layout = QGridLayout()
        self.input_values_layout.setSpacing(1)
        input_values_widget = QWidget()
        input_values_widget.setLayout(self.input_values_layout)

        # add input values layout to input quarter layout
        self.input_quarter_layout = QVBoxLayout()
        self.input_quarter_layout.addWidget(QLabel("<h2>Input values</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.input_quarter_layout.addWidget(input_values_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # add input layout to input widget
        self.general_layout.addLayout(self.input_quarter_layout, 1, 0)

    def _set_output_quarter(self):
        # input values layout
        self.output_values_layout = QGridLayout()
        self.output_values_layout.setSpacing(1)
        output_values_widget = QWidget()
        output_values_widget.setLayout(self.output_values_layout)

        # add output values layout to output quarter layout
        self.output_quarter_layout = QVBoxLayout()
        self.output_quarter_layout.addWidget(QLabel("<h2>Output values</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.output_quarter_layout.addWidget(output_values_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.general_layout.addLayout(self.output_quarter_layout, 0, 1)

    def _set_graph_quarter(self):
        self.graph_values_layout = QGridLayout()
        self.graph_values_layout.setSpacing(1)
        graph_values_widget = QWidget()
        graph_values_widget.setLayout(self.graph_values_layout)
        # scroll
        graph_scroll = QScrollArea()
        graph_scroll.setWidgetResizable(True)
        graph_scroll.setFixedSize(SCROLL_WIDTH, SCROLL_HEIGHT)
        graph_scroll.setFrameShape(QFrame.Shape.NoFrame)
        graph_scroll.setWidget(graph_values_widget)

        # Lmax
        self.lmax_label = QLabel("")
        # self.lmax_label.setStyleSheet("font-size:15px")


        self.graph_quarter_layout = QVBoxLayout()
        self.graph_quarter_layout.addWidget(QLabel("<h2>Graph</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.graph_quarter_layout.addWidget(graph_scroll, alignment=Qt.AlignmentFlag.AlignCenter)
        self.graph_quarter_layout.addWidget(self.lmax_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.general_layout.addLayout(self.graph_quarter_layout, 1, 1)

    def _clear_user_values(self):
        print("[Start] _clear_user_values")
        self.user_min_time.setText("")
        self.user_max_time.setText("")
        self.user_tasks_number.setText("")
        self.user_min_time.setFocus()
        print("[End]   _clear_user_values")

    def get_user_values(self) -> dict:
        print("[Start] get_user_values")
        user_values = {
            "min_time": self.user_min_time.text(),
            "max_time": self.user_max_time.text(),
            "tasks_number": self.user_tasks_number.text()
        }
        print(f"[End] get_user_values, returning: {user_values}")
        return user_values
