from tests.base.base_test import BaseFileSystemTest
from tests.base.structures import File, Directory
import os
from src.folder_admin.folder_admin import run_folder_admin, validate_config_file, create_config_file, \
    ValidateConfigStatus, \
    ValidateConfigErrorMessage, Extensions
import unittest
import json
from typing import List, Tuple


class TestRunFolderAdmin(BaseFileSystemTest, unittest.TestCase):
    test_folder = "./tmp/test_folder"
    files = [
        File("file1.txt", "file1 content"),
        File("file2.txt", "file2 content"),
        File("file3.txt", "file3 content"),
        File("audio.mp3", ""),
        File("video.mp4", ""),
        File("FolderAdministratorConfig.json", '''
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
            '''),
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

    def test_normal_folder_structure(self):
        self.setup_test_folder()

        self.execute_in_test_folder(run_folder_admin)
        current_state = self.get_test_folder_state()
        self.clear_test_folder()
        self.assertEqual(current_state, self.expected_state)

    def test_with_existing_folders(self):
        self.directories = [
            Directory(name="audio"),
            Directory(name="video"),
            Directory(name="documents"),
        ]
        self.setup_test_folder()

        self.execute_in_test_folder(run_folder_admin)
        current_state = self.get_test_folder_state()
        self.clear_test_folder()
        self.assertEqual(current_state, self.expected_state)

    def test_with_partly_existing_folders(self):
        self.directories = [
            Directory(name="audio"),
        ]
        self.setup_test_folder()

        self.execute_in_test_folder(run_folder_admin)
        current_state = self.get_test_folder_state()
        self.clear_test_folder()
        self.assertEqual(current_state, self.expected_state)

    def test_with_empty_config_file(self):
        files_with_empty_config = self.files.copy()
        files_with_empty_config[-1] = File("FolderAdministratorConfig.json", "[]")
        self.setup_test_folder(files=files_with_empty_config)
        self.execute_in_test_folder(run_folder_admin)
        self.assertEqual(self.get_test_folder_state(),
                         Directory(name="test_folder", files=files_with_empty_config, subdirectories=[]))
        self.clear_test_folder()


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
        self.assertEqual(self.execute_in_test_folder(validate_config_file), ([], ValidateConfigStatus.VALID))
        self.clear_test_folder()

    def __base_test_invalid_config_file(self, config_file_content,
                                        expected_output: Tuple[List[ValidateConfigErrorMessage], ValidateConfigStatus]):
        self.files = [
            File("FolderAdministratorConfig.json", config_file_content)
        ]
        self.setup_test_folder()
        self.assertEqual(self.execute_in_test_folder(validate_config_file), expected_output)
        self.clear_test_folder()

    def test_invalid_config_file_invalid_json(self):
        self.__base_test_invalid_config_file("not a json,,,{{{",
                                             ([ValidateConfigErrorMessage.INVALID_JSON_FORMAT],
                                              ValidateConfigStatus.WRONG_STRUCTURE))

    def test_invalid_config_file_not_a_list(self):
        self.__base_test_invalid_config_file("{}",
                                             ([ValidateConfigErrorMessage.NOT_A_LIST],
                                              ValidateConfigStatus.WRONG_STRUCTURE))

    def test_invalid_config_file_not_a_list_of_dicts(self):
        self.__base_test_invalid_config_file('["a", "b", "c"]',
                                             ([ValidateConfigErrorMessage.NOT_A_DICT],
                                              ValidateConfigStatus.WRONG_STRUCTURE))


class TestCreateConfigFile(BaseFileSystemTest, unittest.TestCase):
    test_folder = "./tmp/test_folder"

    extensions = [Extensions.CODES, Extensions.DOCUMENTS, Extensions.VIDEO, Extensions.AUDIO]
    expected_config_file = [
            {
                "dirname": "codes",
                "extensions": Extensions.CODES.value,
            },
            {
                "dirname": "documents",
                "extensions": Extensions.DOCUMENTS.value,
            },
            {
                "dirname": "video",
                "extensions": Extensions.VIDEO.value,
            },
            {
                "dirname": "audio",
                "extensions": Extensions.AUDIO.value,
            }
        ]

    def __read_config_file(self) -> List[dict]:
        def fn() -> List[dict]:
            with open("FolderAdministratorConfig.json", "r") as file:
                f_string = file.read()
                return json.loads(f_string)

        return self.execute_in_test_folder(fn)

    def __extensions_to_string(self, extensions: list) -> str:
        return ",".join(extensions)

    def test_config_file_does_not_exist(self):
        self.setup_test_folder()
        self.execute_in_test_folder(
            lambda: create_config_file(self.extensions))
        self.assertEqual(self.__read_config_file(), self.expected_config_file)
        self.clear_test_folder()

    def test_rewrite_existing_config_file(self):
        self.files = [
            File("FolderAdministratorConfig.json", "some random stuff to be rewritten")]
        self.setup_test_folder()
        self.execute_in_test_folder(
            lambda: create_config_file(self.extensions))
        self.assertEqual(self.__read_config_file(), self.expected_config_file)
        self.clear_test_folder()
