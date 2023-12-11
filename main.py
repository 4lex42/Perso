import argparse
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

import pyzipper


class ZipFolderWithPassword:
    def __init__(self):
        self.folder_path = ""
        self.destination_folder = ""
        self.zip_filename = ""
        self.password = ""

    def get_user_input(self):
        # get the inputs with GUI
        root = tk.Tk()
        root.withdraw()

        self.folder_path = filedialog.askdirectory(title="Sélectionnez le dossier à sécuriser")
        if self.folder_path == "":
            return False
        self.destination_folder = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        if self.destination_folder == "":
            return False
        self.zip_filename = simpledialog.askstring("Nom du fichier ZIP", "Entrez le nom du fichier ZIP")
        if self.zip_filename == "":
            return False
        self.password = simpledialog.askstring("Mot de passe", "Entrez le mot de passe")
        if self.password == "":
            return False

        root.destroy()

    def zip_folder(self):
        # zip the folder
        try:
            zip_path = os.path.join(self.destination_folder, self.zip_filename)
            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                     encryption=pyzipper.WZ_AES) as zip_file:
                zip_file.pwd = self.password.encode('utf-8')  # Set the password directly

                # Parcours tous les fichiers du dossier
                for foldername, subfolders, filenames in os.walk(self.folder_path):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, self.folder_path)

                        # Vérifie si le fichier existe déjà dans l'archive et le remplace
                        if arcname in zip_file.NameToInfo:
                            zip_file.replace(arcname, file_path)
                        else:
                            zip_file.write(file_path, arcname)

        except Exception as e:
            print(f"An error occurred: {e}")

    def sort_files_by_name(self):
        # sort files by alphabetic
        try:
            # Liste tous les fichiers dans le dossier
            files = sorted(os.listdir(self.folder_path))
            sorted_files = [os.path.join(self.folder_path, file) for file in files if
                            os.path.isfile(os.path.join(self.folder_path, file))]
            return sorted_files

        except Exception as e:
            print(f"An error occurred while sorting files: {e}")


class CommandLineZipper:
    def __init__(self, folder_path, destination_folder, zip_filename, password):
        self.zip_handler = ZipFolderWithPassword()
        self.zip_handler.folder_path = folder_path
        self.zip_handler.destination_folder = destination_folder
        self.zip_handler.zip_filename = zip_filename
        self.zip_handler.password = password

    def execute_zip_command(self):
        # execute the zip
        try:
            self.zip_handler.zip_folder()
            print("Zip operation completed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description="Zip a folder with password protection. \n")
    parser.add_argument("--folder_path", help="Path to the folder to be zipped. \n")
    parser.add_argument("--destination_folder", help="Path to the destination folder. \n")
    parser.add_argument("--zip_filename", help="Name of the ZIP file. \n")
    parser.add_argument("--password", help="Password for ZIP file encryption. \n")

    args = parser.parse_args()

    if args.folder_path and args.destination_folder and args.zip_filename and args.password:
        # Command line mode
        cmd_zipper = CommandLineZipper(args.folder_path, args.destination_folder, args.zip_filename, args.password)
        cmd_zipper.execute_zip_command()
    else:
        # GUI mode
        zip_handler = ZipFolderWithPassword()
        zip_handler.get_user_input()
        zip_handler.zip_folder()


if __name__ == "__main__":
    main()
