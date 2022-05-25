from rust_toolkit import FolderAdministrator
from enum import Enum
import os
import json
from typing import Optional, List
import cli

class ValidateConfigStatus(Enum):
    VALID = 0
    DOES_NOT_EXIST = 1
    WRONG_STRUCTURE = 2


class ValidateConfigErrorMessage(Enum):
    DOES_NOT_EXIST = ("Config file does not exist.",)
    INVALID_JSON_FORMAT = ("Config file should be a in a valid JSON format.",)
    NOT_A_LIST = ("Config file should be a list.",)
    NOT_A_DICT = ("Values of config list should be valid dictionaries.",)
    MISSING_DIRNAME = ("Every config value should have 'dirname' key.",)
    MISSING_EXTENSIONS = (
        "Every config value should have 'extensions' key which is list of file extensions without 'dot' ('.')'",)
    INVALID_EXTENSIONS = ("Extensions should be defined without 'dot' as the first character.",)


def folder_admin():
    err_msg, config_file_state = validate_config_file()
    run_folder_admin()


def validate_config_file() -> (List[ValidateConfigErrorMessage], ValidateConfigStatus):
    err_msg = []
    status: ValidateConfigStatus = ValidateConfigStatus.VALID

    # check if config file exists
    if not os.path.exists("FolderAdministratorConfig.json"):
        err_msg.append(ValidateConfigErrorMessage.DOES_NOT_EXIST)
        return err_msg, ValidateConfigStatus.DOES_NOT_EXIST

    with open("FolderAdministratorConfig.json", "r") as config_file:
        config_file_content = config_file.read()
        try:
            config = json.loads(config_file_content)
        except json.decoder.JSONDecodeError:
            err_msg.append(ValidateConfigErrorMessage.INVALID_JSON_FORMAT)
            return err_msg, ValidateConfigStatus.WRONG_STRUCTURE

    if not isinstance(config, list):
        err_msg.append(ValidateConfigErrorMessage.NOT_A_LIST)
        return err_msg, ValidateConfigStatus.WRONG_STRUCTURE

    # check if config file has correct structure
    for config_item in config:
        if not isinstance(config_item, dict):
            if ValidateConfigErrorMessage.NOT_A_DICT not in err_msg:
                err_msg.append(ValidateConfigErrorMessage.NOT_A_DICT)
            status = ValidateConfigStatus.WRONG_STRUCTURE
            continue

        if not config_item.get("dirname"):
            if ValidateConfigErrorMessage.MISSING_DIRNAME not in err_msg:
                err_msg.append(ValidateConfigErrorMessage.MISSING_DIRNAME)
            status = ValidateConfigStatus.WRONG_STRUCTURE
            continue

        if not config_item.get("extensions"):
            if ValidateConfigErrorMessage.MISSING_EXTENSIONS not in err_msg:
                err_msg.append(ValidateConfigErrorMessage.MISSING_EXTENSIONS)
            status = ValidateConfigStatus.WRONG_STRUCTURE
            continue

        if not isinstance(config_item.get("extensions"), list):
            if ValidateConfigErrorMessage.NOT_A_LIST not in err_msg:
                err_msg.append(ValidateConfigErrorMessage.NOT_A_LIST)
            status = ValidateConfigStatus.WRONG_STRUCTURE
            continue

        for extension in config_item.get("extensions"):
            if extension[0] == ".":
                if ValidateConfigErrorMessage.INVALID_EXTENSIONS not in err_msg:
                    err_msg.append(ValidateConfigErrorMessage.INVALID_EXTENSIONS)
                status = ValidateConfigStatus.WRONG_STRUCTURE
                break

    return err_msg, status


def run_folder_admin(verbose: bool = False):
    admin = FolderAdministrator(verbose)
    admin.move_files_to_dirs()


# executor for debug purposes
if __name__ == "__main__":
    folder_admin()
