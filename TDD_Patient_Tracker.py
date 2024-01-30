import unittest
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication
from main import Information, UserProfile, SecurityCenter, DataCenter, UpToDateCenter, UserInterface


class TestInformation(unittest.TestCase):
    def test_information_creation(self):
        info = Information("MentalInfo", "PhysicalInfo")
        self.assertEqual(info.Mental_Health_Info, "MentalInfo")
        self.assertEqual(info.Physical_Health_Info, "PhysicalInfo")


class TestUserProfile(unittest.TestCase):
    def test_user_profile_creation(self):
        info = Information("MentalInfo", "PhysicalInfo")
        user_profile = UserProfile("1", info, "username", "password")
        self.assertEqual(user_profile.ID, "1")
        self.assertEqual(user_profile.Information, info)
        self.assertEqual(user_profile.username, "username")
        self.assertEqual(user_profile.password, "password")


class TestUserInterface(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.data_center = DataCenter()
        self.up_to_date_center = UpToDateCenter()
        self.security_center = SecurityCenter(self.data_center, self.up_to_date_center)

    def test_display_information_success(self):
        ui = UserInterface(self.security_center, self.data_center, self.up_to_date_center)
        self.security_center.user_security_info = pd.DataFrame([
            {'username': 'arash', 'password': 'arash_1380', 'ID': '1'}
        ])
        self.data_center.data_frame = pd.DataFrame(columns=['ID', 'Information'])
        self.data_center.data_frame = self.data_center.data_frame.append(
            {'ID': '1', 'Information': Information("MentalInfo", "PhysicalInfo")}, ignore_index=True)
        ui.username_edit.setText('arash')
        ui.password_edit.setText('arash_1380')
        ui.display_information()
        self.assertEqual(ui.result_label.text(), "Displaying Information: MentalInfo, PhysicalInfo")

    def test_display_information_failure(self):
        ui = UserInterface(self.security_center, self.data_center, self.up_to_date_center)
        self.security_center.user_security_info = pd.DataFrame([
            {'username': 'arash', 'password': 'arash_1380', 'ID': '1'}
        ])
        ui.username_edit.setText('arash')
        ui.password_edit.setText('qefig2342rhi2')
        ui.display_information()
        self.assertEqual(ui.result_label.text(), "Failed to display information / User has no permission!")

    def test_insert_information_success(self):
        ui = UserInterface(self.security_center, self.data_center, self.up_to_date_center)
        self.security_center.user_security_info = pd.DataFrame([
            {'username': 'navid', 'password': 'nd_kianfar', 'ID': '2'}
        ])
        self.data_center.data_frame = pd.DataFrame(columns=['ID', 'Information'])
        ui.username_edit.setText('navid')
        ui.password_edit.setText('nd_kianfar')
        ui.insert_information()
        self.assertEqual(ui.result_label.text(), "Information inserted successfully!")

    def test_insert_information_failure(self):
        ui = UserInterface(self.security_center, self.data_center, self.up_to_date_center)
        self.security_center.user_security_info = pd.DataFrame([
            {'username': 'arash', 'password': 'arash_1380', 'ID': '1'}
        ])
        ui.username_edit.setText('arash')
        ui.password_edit.setText('qfqf3reqef')
        ui.insert_information()
        self.assertEqual(ui.result_label.text(), "Failed to insert information / User has no permission!")


class TestSecurityCenter(unittest.TestCase):
    def setUp(self):
        self.data_center = DataCenter()
        self.up_to_date_center = UpToDateCenter()
        self.security_center = SecurityCenter(self.data_center, self.up_to_date_center)

    def test_check_permission_success(self):
        self.security_center.user_security_info = pd.DataFrame([
            {'username': 'arash', 'password': 'arash_1380', 'ID': '1'}
        ])
        result, user_id = self.security_center.check_permission('arash', 'arash_1380', 'retrieve')
        self.assertEqual(result, "success")
        self.assertEqual(user_id, '1')

    def test_check_permission_failure(self):
        self.security_center.user_security_info = pd.DataFrame([
            {'username': 'arash', 'password': 'arash_1380', 'ID': '1'}
        ])
        result, user_id = self.security_center.check_permission('arash', 'kiduawd2weq23', 'retrieve')
        self.assertEqual(result, "failure")
        self.assertIsNone(user_id)

    def test_inform_of_insert(self):
        self.data_center.insert_requests = set()
        self.security_center.inform_of_insert('1')
        self.assertEqual(self.data_center.insert_requests, {'1'})

    def test_send_for_insert(self):
        self.security_center.send_for_insert('1')
        self.assertEqual(self.data_center.data_frame.loc['1', 'Information'].Mental_Health_Info, 'MentalInfo')
        self.assertEqual(self.data_center.data_frame.loc['1', 'Information'].Physical_Health_Info, 'PhysicalInfo')


class TestDataCenter(unittest.TestCase):
    def setUp(self):
        self.data_center = DataCenter()

    def test_check_insert(self):
        self.data_center.insert_requests = {'1', '2'}
        self.assertTrue(self.data_center.check_insert('1'))
        self.assertFalse(self.data_center.check_insert('3'))

    def test_insert_success(self):
        self.data_center.insert_requests = {'1'}
        info = Information("MentalInfo", "PhysicalInfo")
        result = self.data_center.insert('1', info)
        self.assertTrue(result)
        self.assertEqual(self.data_center.data_frame.loc['1', 'Information'].Mental_Health_Info, 'MentalInfo')
        self.assertEqual(self.data_center.data_frame.loc['1', 'Information'].Physical_Health_Info, 'PhysicalInfo')

    def test_insert_failure(self):
        self.data_center.insert_requests = {'2'}
        info = Information("MentalInfo", "PhysicalInfo")
        result = self.data_center.insert('1', info)
        self.assertFalse(result)
        self.assertTrue(self.data_center.data_frame.empty)

    def test_retrieve(self):
        info = self.data_center.retrieve('1')
        self.assertEqual(info.Mental_Health_Info, 'RetrievedMentalInfo')
        self.assertEqual(info.Physical_Health_Info, 'RetrievedPhysicalInfo')


class TestUpToDateCenter(unittest.TestCase):
    def setUp(self):
        self.up_to_date_center = UpToDateCenter()

    def test_insert(self):
        info = Information("MentalInfo", "PhysicalInfo")
        self.up_to_date_center.insert('1', info)
        self.assertEqual(self.up_to_date_center.data_frame.loc['1', 'Information'].Mental_Health_Info, 'MentalInfo')
        self.assertEqual(self.up_to_date_center.data_frame.loc['1', 'Information'].Physical_Health_Info, 'PhysicalInfo')

    def test_retrieve(self):
        info = self.up_to_date_center.retrieve('1')
        self.assertEqual(info.Mental_Health_Info, 'MentalInfo')
        self.assertEqual(info.Physical_Health_Info, 'PhysicalInfo')


if __name__ == '__main__':
    unittest.main()
