import argparse
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

import pyzipper


class UserInterface:
    def __init__(self):
        """
        Initialize UserInterface instance.

        PRE: None
        POST: Initializes the instance.
        """
        self.zip_handler = ZipFolderWithPassword()

    def run(self, args=None):
        """
        Run the user interface based on the provided arguments.

        PRE: None
        POST: If command-line arguments are provided, it executes the zip operation in command-line mode.
              If no command-line arguments are provided, it initiates the GUI mode
              to collect user input and perform the zip operation.
        """
        parser = argparse.ArgumentParser(description="Zip a folder with password protection. \n")
        parser.add_argument("--folder_path", help="Path to the folder to be zipped. \n")
        parser.add_argument("--destination_folder", help="Path to the destination folder. \n")
        parser.add_argument("--zip_filename", help="Name of the ZIP file. \n")
        parser.add_argument("--password", help="Password for ZIP file encryption. \n")

        args = parser.parse_args(args)

        if args.folder_path and args.destination_folder and args.zip_filename and args.password:
            # Command line mode
            cmd_zipper = CommandLineZipper(args.folder_path, args.destination_folder, args.zip_filename, args.password)
            cmd_zipper.execute_zip_command()
        else:
            # GUI mode
            self.gui_mode()

    def gui_mode(self):
        """
        Run the GUI mode to collect user input and perform the zip operation.

        PRE: None
        POST: None
        """
        success = self.get_user_input()
        if success:
            self.zip_handler.zip_folder()

    def get_user_input(self):
        """
        Collect user input using a GUI.

        PRE: None
        POST: Returns True if all inputs are received; False otherwise.
        RAISE: ValueError if any of the required input values is not provided.
        """
        root = tk.Tk()
        root.withdraw()

        self.zip_handler.folder_path = filedialog.askdirectory(title="Sélectionnez le dossier à sécuriser")
        if not self.zip_handler.folder_path:
            raise ValueError("Le chemin du dossier à sécuriser doit être spécifié.")

        self.zip_handler.destination_folder = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        if not self.zip_handler.destination_folder:
            raise ValueError("Le chemin du dossier de destination doit être spécifié.")

        self.zip_handler.zip_filename = simpledialog.askstring("Nom du fichier ZIP", "Entrez le nom du fichier ZIP")
        if not self.zip_handler.zip_filename:
            raise ValueError("Le nom du fichier ZIP doit être spécifié.")

        self.zip_handler.password = simpledialog.askstring("Mot de passe", "Entrez le mot de passe")
        if not self.zip_handler.password:
            raise ValueError("Le mot de passe doit être spécifié.")

        root.destroy()
        return True


class ZipFolderWithPassword:
    def __init__(self):
        """
        Initialize ZipFolderWithPassword instance.

        PRE: None
        POST: Initializes the instance with empty strings for folder_path,
              destination_folder, zip_filename, and password.
        <---------------------------------------------------------------------------->
        IF ENCAPSULATION:
        def __init__(self):
            self._folder_path = ""
            self._destination_folder = ""
            self._zip_filename = ""
            self._password = ""

        def set_folder_path(self, folder_path):
            self._folder_path = folder_path

        def get_folder_path(self):
            return self._folder_path
        <---------------------------------------------------------------------------->
        """
        self.folder_path = ""
        self.destination_folder = ""
        self.zip_filename = ""
        self.password = ""

    def zip_folder(self):
        """
        Zip the folder with password protection.

        PRE: Assumes that get_user_input has been called successfully.
        POST: Prints an error message if an exception occurs during zipping.
        RAISE: ValueError if any of the required parameters for ZIP compression is not correctly defined.
               RuntimeError if any other error occurs during zipping.
        """
        if not (self.folder_path and self.destination_folder and self.zip_filename and self.password):
            raise ValueError("Tous les paramètres requis pour la compression ZIP doivent être définis correctement.")

        try:
            zip_path = os.path.join(self.destination_folder, self.zip_filename)
            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                     encryption=pyzipper.WZ_AES) as zip_file:
                zip_file.pwd = self.password.encode('utf-8')  # Set the password directly

                for foldername, subfolders, filenames in os.walk(self.folder_path):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, self.folder_path)

                        if arcname in zip_file.NameToInfo:
                            zip_file.replace(arcname, file_path)
                        else:
                            zip_file.write(file_path, arcname)

        except Exception as e:
            raise RuntimeError(f"An error occurred during zipping: {e}")


class CommandLineZipper:
    def __init__(self, folder_path, destination_folder, zip_filename, password):
        """
        Initialize CommandLineZipper instance.

        PRE: None
        POST: Initializes the instance with the provided values for
              folder_path, destination_folder, zip_filename, and password.
        """
        self.zip_handler = ZipFolderWithPassword()
        self.zip_handler.folder_path = folder_path
        self.zip_handler.destination_folder = destination_folder
        self.zip_handler.zip_filename = zip_filename
        self.zip_handler.password = password

    def execute_zip_command(self):
        """
        Execute the zip command in command-line mode.

        PRE: Assumes that command-line arguments are provided.
        POST: Prints an error message if an exception occurs during zipping.
        RAISE: RuntimeError if any error occurs during zipping.
        """
        try:
            self.zip_handler.zip_folder()
            print("Zip operation completed successfully.")
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")


if __name__ == "__main__":
    ui = UserInterface()
    try:
        ui.run()
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except RuntimeError as re:
        print(f"RuntimeError: {re}")
