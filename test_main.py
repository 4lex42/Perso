import unittest
from io import StringIO
from unittest.mock import MagicMock

from main import UserInterface, ZipFolderWithPassword, CommandLineZipper


class TestZipperFunctions(unittest.TestCase):

    def test_get_user_input(self):
        ui = UserInterface()
        ui.zip_handler = ZipFolderWithPassword()

        with unittest.mock.patch('builtins.input', side_effect=['C:/Users/alexl/Downloads/Admin',
                                                                'C:/Users/alexl/Downloads/Admin2', 'output.zip',
                                                                'password123']):
            self.assertTrue(ui.get_user_input())
            self.assertEqual(ui.zip_handler.folder_path, 'C:/Users/alexl/Downloads/Admin')
            self.assertEqual(ui.zip_handler.destination_folder, 'C:/Users/alexl/Downloads/Admin2')
            self.assertEqual(ui.zip_handler.zip_filename, 'output.zip')
            self.assertEqual(ui.zip_handler.password, 'password123')

    def test_gui_mode(self):
        ui = UserInterface()
        ui.zip_handler = MagicMock()
        ui.zip_handler.folder_path = 'C:/Users/alexl/Downloads/Admin'
        ui.zip_handler.destination_folder = 'C:/Users/alexl/Downloads/Admin2'
        ui.zip_handler.zip_filename = 'output.zip'
        ui.zip_handler.password = 'password123'

        with unittest.mock.patch('tkinter.filedialog.askdirectory', side_effect=['C:/Users/alexl/Downloads/Admin',
                                                                                 'C:/Users/alexl/Downloads/Admin2']):
            with unittest.mock.patch('tkinter.simpledialog.askstring', side_effect=['output.zip', 'password123']):
                ui.gui_mode()
                ui.zip_handler.zip_folder.assert_called_once()

    def test_zip_folder(self):
        zip_handler = ZipFolderWithPassword()
        zip_handler.folder_path = 'C:/Users/alexl/Downloads/Admin'
        zip_handler.destination_folder = 'C:/Users/alexl/Downloads/Admin2'
        zip_handler.zip_filename = 'output.zip'
        zip_handler.password = 'password123'

        with unittest.mock.patch('os.path.join', return_value='C:/Users/alexl/Downloads/Admin2/output.zip'), \
                unittest.mock.patch('pyzipper.AESZipFile'), \
                unittest.mock.patch('os.walk', return_value=[('C:/Users/alexl/Downloads/Admin', [], ['file.txt'])]):
            zip_handler.zip_folder()

    def test_command_line_zipper(self):
        cmd_zipper = CommandLineZipper('C:/Users/alexl/Downloads/Admin', 'C:/Users/alexl/Downloads/Admin2',
                                       'output.zip', 'password123')
        with unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            cmd_zipper.execute_zip_command()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "Zip operation completed successfully.")


if __name__ == '__main__':
    unittest.main()
