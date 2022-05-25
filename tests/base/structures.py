from typing import List


class File:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class Directory:
    def __init__(self, name: str = None, files: List[File] = None, subdirectories: List['Directory'] = None):
        self.name = name
        self.files = files
        self.subdirectories = subdirectories

    def __eq__(self, other) -> bool:
        # Check if name is equal
        output = self.name == other.name

        if not output:
            return output

        filenames = [file.name for file in self.files]
        other_filenames = [file.name for file in other.files]

        # Check if there is same number of files
        output &= len(filenames) == len(other_filenames)

        if not output:
            return output

        # Check if files have same names
        for filename in filenames:
            output &= filename in other_filenames

        if not output:
            return output

        subdir_names = [subdir.name for subdir in self.subdirectories]
        other_subdir_names = [subdir.name for subdir in other.subdirectories]

        # Check if there is same number of subdirectories
        output &= len(subdir_names) == len(other_subdir_names)

        if not output:
            return output

        # Check if subdirectories have same names
        for subdir_name in subdir_names:
            output &= subdir_name in other_subdir_names

        if not output:
            return output

        # if everything is equal, check if subdirectories are equal
        # check if subdirectories have same number of files

        for index, subdir in enumerate(self.subdirectories):
            output &= len(subdir.files) == len([file.name for file in other.subdirectories[index].files])
            # if ok then check if files have same names
            if not output:
                return output
            for file in subdir.files:
                output &= file.name in [file.name for file in other.subdirectories[index].files]

        return output
