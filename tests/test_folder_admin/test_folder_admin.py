from tests.base.base_test import BaseFileSystemTest
from tests.base.structures import File, Directory
import os
from src.folder_admin import folder_admin

class TestFolderAdmin(BaseFileSystemTest):
    test_folder = "./tmp/test_folder"

    def test_normal_folder_structure(self):
        self.files = [
            File("file1.txt", "file1 content"),
            File("file2.txt", "file2 content"),
            File("file3.txt", "file3 content"),
            File("audio.mp3", ""),
            File("video.mp4", ""),
            File("FolderAdministratorConfig.json",
                 '''
            [
                {
                    "dirname": "audio",
                    "extensions": ["mp3"]
                },
                {
                    "dirname": "video",
                    "extensions": ["mp4"]
                },
                {
                    "dirname": "documents",
                    "extensions": ["txt"]
                }
            ]
            ''')
        ]

        expected_state = Directory(
            name="test_folder",
            files=[File("FolderAdministratorConfig.json", "")],
            subdirectories=[
                Directory(
                    name="audio",
                    files=[File("audio.mp3", "")]
                ),
                Directory(
                    name="documents",
                    files=[File("file1.txt", "file1 content"), File(
                        "file2.txt", "file2 content"), File("file3.txt", "file3 content")],
                ),
                Directory(
                    name="video",
                    files=[File("video.mp4", "")],
                )]

        )
        self.setup_test_folder()

        current_path = os.path.abspath(os.getcwd())
        os.chdir(self.test_folder)
        print(f'CURRENT DIR {os.getcwd()}')
        folder_admin.folder_admin()
        os.chdir(current_path)

        assert self.get_test_folder_state() == expected_state
        self.clear_test_folder()
