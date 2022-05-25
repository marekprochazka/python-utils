from tests.base.base_test import BaseFileSystemTest
from tests.base.structures import File, Directory
import os
from src.folder_admin.folder_admin import run_folder_admin, validate_config_file, ValidateConfigStatus, \
    ValidateConfigErrorMessage
import unittest


class TestRunFolderAdmin(BaseFileSystemTest, unittest.TestCase):
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

        self.execute_in_test_folder(run_folder_admin)
        current_state = self.get_test_folder_state()
        self.clear_test_folder()
        self.assertEqual(current_state, expected_state)


class TestValidateConfigFile(BaseFileSystemTest, unittest.TestCase):
    test_folder = "./tmp/test_folder"

    def test_config_file_does_not_exist(self):
        self.setup_test_folder()
        self.assertEqual(self.execute_in_test_folder(validate_config_file),
                         ([ValidateConfigErrorMessage.DOES_NOT_EXIST], ValidateConfigStatus.DOES_NOT_EXIST))
        self.clear_test_folder()

    def test_config_valid(self):
        self.files = [
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
        self.setup_test_folder()
        self.assertNotEqual(self.execute_in_test_folder(validate_config_file), ([], ValidateConfigStatus.VALID))
        self.clear_test_folder()
