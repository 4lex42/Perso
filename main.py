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
        root = tk.Tk()
        root.withdraw()

        self.folder_path = filedialog.askdirectory(title="Sélectionnez le dossier à sécuriser")
        self.destination_folder = filedialog.askdirectory(title="Sélectionnez le dossier de destination")
        self.zip_filename = simpledialog.askstring("Nom du fichier ZIP", "Entrez le nom du fichier ZIP")
        self.password = simpledialog.askstring("Mot de passe", "Entrez le mot de passe")

        root.destroy()

    def zip_folder(self):
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
        try:
            # Liste tous les fichiers dans le dossier
            files = sorted(os.listdir(self.folder_path))
            sorted_files = [os.path.join(self.folder_path, file) for file in files if
                            os.path.isfile(os.path.join(self.folder_path, file))]
            return sorted_files

        except Exception as e:
            print(f"An error occurred while sorting files: {e}")


def main():
    try:
        zip_handler = ZipFolderWithPassword()
        zip_handler.get_user_input()
        zip_handler.zip_folder()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
