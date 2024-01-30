# Group 9 - Arash Foroozanfar - Navid Kianfar - Ali Hushemian
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import pandas as pd


class Information:
    def __init__(self, mental_health_info, physical_health_info):
        self.Mental_Health_Info = mental_health_info
        self.Physical_Health_Info = physical_health_info


class UserProfile:
    def __init__(self, user_id, information, username, password):
        self.ID = user_id
        self.Information = information
        self.username = username
        self.password = password


class UserInterface(QWidget):
    def __init__(self, security_center, data_center, up_to_date_center):
        super().__init__()

        self.security_center = security_center
        self.data_center = data_center
        self.up_to_date_center = up_to_date_center

        self.init_ui()

    def init_ui(self):
        self.username_label = QLabel('Username:')
        self.username_edit = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_edit = QLineEdit()

        self.display_button = QPushButton('Display Information')
        self.insert_button = QPushButton('Insert Information')

        self.result_label = QLabel('Result:')

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.display_button)
        layout.addWidget(self.insert_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.display_button.clicked.connect(self.display_information)
        self.insert_button.clicked.connect(self.insert_information)

        self.setWindowTitle('Patient Tracker')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def display_information(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        result, user_id = self.security_center.check_permission(username, password, "retrieve")

        if result == "success":
            user_info = self.data_center.retrieve(user_id)
            self.result_label.setText(
                f"Displaying Information: {user_info.Mental_Health_Info}, {user_info.Physical_Health_Info}")
        else:
            self.result_label.setText("Failed to display information / User has no permission!")

    def insert_information(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        result, user_id = self.security_center.check_permission(username, password, "insert")

        if result == "success":
            self.security_center.inform_of_insert(user_id)
            self.security_center.send_for_insert(user_id)
            self.result_label.setText("Information inserted successfully!")
        else:
            self.result_label.setText("Failed to insert information / User has no permission!")


class SecurityCenter:
    def __init__(self, data_center, up_to_date_center, initial_users=None):
        if initial_users is None:
            initial_users = []
        self.user_security_info = pd.DataFrame(initial_users)
        self.user_id = None
        self.data_center = data_center
        self.up_to_date_center = up_to_date_center

    def check_permission(self, username, password, intent):
        match = self.user_security_info[
            (self.user_security_info['username'] == username) & (self.user_security_info['password'] == password)]

        if not match.empty:
            if intent == "retrieve" or intent == "insert":
                self.user_id = match['ID'].values[0]
                return "success", self.user_id
        return "failure", None

    def inform_of_insert(self, user_id):
        self.data_center.insert_requests.add(user_id)

    def insert_information(self, user_id, information):
        result = self.data_center.insert(user_id, information)

        if result:
            self.up_to_date_center.insert(user_id, information)

    def send_for_insert(self, user_id):
        self.insert_information(user_id, Information("MentalInfo", "PhysicalInfo"))


class DataCenter:
    def __init__(self):
        self.insert_requests = set()
        self.data_frame = pd.DataFrame(columns=['ID', 'Information'])

    def check_insert(self, user_id):
        return user_id in self.insert_requests

    def insert(self, user_id, information):
        if self.check_insert(user_id):
            self.data_frame = self.data_frame.append({'ID': user_id, 'Information': information}, ignore_index=True)
            print("Inserted information in Data Center:", information)
            return True
        else:
            print("Failed to insert information in Data Center.")
            return False

    def retrieve(self, user_id):
        return Information("MentalInfo", "PhysicalInfo")


class UpToDateCenter:
    def __init__(self):
        self.data_frame = pd.DataFrame(columns=['ID', 'Information'])

    def insert(self, user_id, information):
        self.data_frame = self.data_frame.append({'ID': user_id, 'Information': information}, ignore_index=True)
        print("Inserted information in UpToDateCenter:", information)

    def retrieve(self, user_id):
        retrieved_info = self.data_frame[self.data_frame['ID'] == user_id]['Information'].values[0]
        print("Retrieved information from UpToDateCenter:", retrieved_info)
        return retrieved_info


def main():
    app = QApplication(sys.argv)

    data_center = DataCenter()
    up_to_date_center = UpToDateCenter()

    initial_users = [
        {'username': 'arash', 'password': 'arash_1380', 'ID': '1'},
        {'username': 'navid', 'password': 'nd_kianfar', 'ID': '2'}
    ]

    security_center = SecurityCenter(data_center, up_to_date_center, initial_users)

    ui = UserInterface(security_center, data_center, up_to_date_center)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
