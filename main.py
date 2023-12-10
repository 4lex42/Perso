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
        root.withdraw()  # Hide the main window

        # Chemin du dossier à sécuriser
        self.folder_path = filedialog.askdirectory(title="Sélectionnez le dossier à sécuriser")

        # Choisissez le dossier où vous voulez stocker le fichier sécurisé
        self.destination_folder = filedialog.askdirectory(title="Sélectionnez le dossier de destination")

        # Choisir un nom de fichier pour l'archive ZIP
        self.zip_filename = simpledialog.askstring("Nom du fichier ZIP", "Entrez le nom du fichier ZIP")

        # Mot de passe à définir
        self.password = simpledialog.askstring("Mot de passe", "Entrez le mot de passe")

        root.destroy()  # Close the Tkinter window

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

                        # Ajoute chaque fichier à l'archive
                        arcname = os.path.relpath(file_path, self.folder_path)
                        zip_file.write(file_path, arcname)

        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    try:
        zip_handler = ZipFolderWithPassword()
        zip_handler.get_user_input()
        zip_handler.zip_folder()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
