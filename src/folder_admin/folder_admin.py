from rust_toolkit import FolderAdministrator

def folder_admin(cli_controller):
    print("STARTING...")
    admin = FolderAdministrator(True)
    admin.move_files_to_dirs()