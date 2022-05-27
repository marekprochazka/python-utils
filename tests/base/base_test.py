import os
from typing import List, Callable, Any, Optional
from abc import ABC
from tests.folder_admin.structures import File, Directory
import shutil


class BaseTest(ABC):
    key_inputs: List[str] = None


class BaseFileSystemTest(BaseTest):
    files: List[File] = None
    directories: List[Directory] = None
    test_folder: str = None

    def setup_test_folder(self, files: Optional[List[File]] = None,
                          directories: Optional[List[Directory]] = None):
        if not files:
            files = self.files
        if not directories:
            directories = self.directories

        # Check if test folder is defined
        if not self.test_folder:
            raise NotImplementedError("test_folder is not defined in class {}".format(self.__class__.__name__))

        # Clear folder if there are any files
        if os.path.exists(self.test_folder):
            shutil.rmtree(os.path.abspath(self.test_folder))

        # Create test folder if it does not exist
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)

        # Create files and directories
        if files:
            for file in files:
                self.__create_file(file)

        if directories:
            for directory in directories:
                self.__create_directory(directory)

    def clear_test_folder(self):
        if os.path.exists(self.test_folder):
            shutil.rmtree(self.test_folder)

    def get_test_folder_state(self) -> Directory:
        test_folder_state: Directory = Directory(self.test_folder.split("/")[-1], [], [])

        # Get files
        for file in os.listdir(self.test_folder):
            if os.path.isfile(f"{self.test_folder}/{file}"):
                with open(f"{self.test_folder}/{file}", "r") as f:
                    test_folder_state.files.append(File(file, f.read()))

        # Get subdirectories
        for directory in os.listdir(self.test_folder):
            if os.path.isdir(f"{self.test_folder}/{directory}"):
                test_folder_state.subdirectories.append(Directory(directory, [], []))

        # Get subdirectories files
        for directory in test_folder_state.subdirectories:
            for file in os.listdir(f"{self.test_folder}/{directory.name}"):
                if os.path.isfile(f"{self.test_folder}/{directory.name}/{file}"):
                    with open(f"{self.test_folder}/{directory.name}/{file}", "r") as f:
                        directory.files.append(File(file, f.read()))

        return test_folder_state

    def execute_in_test_folder(self, command: Callable) -> Any:
        current_path = os.path.abspath(os.getcwd())
        os.chdir(self.test_folder)
        output = command()
        os.chdir(current_path)
        return output

    def __create_file(self, file: File):
        with open(f"{self.test_folder}/{file.name}", "w") as f:
            f.write(file.content)

    def __create_directory(self, directory: Directory):
        os.makedirs(f"{self.test_folder}/{directory.name}")
        if directory.files:
            for file in directory.files:
                self.__create_file(file)
