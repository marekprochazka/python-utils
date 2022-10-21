from rust_toolkit import FolderAdministrator
from enum import Enum
import os
import json
from typing import Optional, List, Tuple
import cli


class ValidateConfigStatus(Enum):
    VALID = 0
    DOES_NOT_EXIST = 1
    WRONG_STRUCTURE = 2


class ValidateConfigErrorMessage(Enum):
    DOES_NOT_EXIST = "Config file does not exist."
    INVALID_JSON_FORMAT = "Config file should be a in a valid JSON format."
    NOT_A_LIST = "Config file should be a list."
    NOT_A_DICT = "Values of config list should be valid dictionaries."
    MISSING_DIRNAME = "Every config value should have 'dirname' key."
    MISSING_EXTENSIONS = \
        "Every config value should have 'extensions' key which is list of file extensions without 'dot' ('.')'"
    INVALID_EXTENSIONS = "Extensions should be defined without 'dot' as the first character."


class Extensions(Enum):
    AUDIO = ["mp3", "wav", "flac", "ogg", "aac", "m4a"]
    VIDEO = ["mp4", "mkv", "avi", "mov", "wmv", "flv", "mpg", "mpeg"]
    DOCUMENTS = ["txt", "pdf", "doc", "docx", "odt", "ods", "odp", "xls", "xlsx", "csv", "ppt", "pptx"]
    COMPRESSED = ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "z", "lz", "lzma", "lzo", "lz4", "lzop", "tgz"]
    IMAGES = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "psd", "svg", "webp", "heif", "heic", "raw", "jfif"]
    EXECUTABLES = ["exe", "msi", "apk", "deb", "rpm", "dmg", "pkg", "ipa", "appx", "app", "com", "cmd"]
    CODES = ["py", "c", "h", "cpp", "java", "js", "go", "php", "html", "css", "scss", "sass", "less", "json", "xml",
             "yml", "yaml", "toml", "md", "rst", "sh", "bat", "cmd", "rs", "r", "swift", "ts", "m", "mm", "h", "hpp",
             "hh", "hxx", "hpp", "hxx", "cs", "csx", "asm"]


def main():
    err_msg, config_file_state = validate_config_file()
    if config_file_state == ValidateConfigStatus.DOES_NOT_EXIST:
        create_new = cli.CliUtils.yes_no(question=[cli.WinString(err_msg[0].value, cli.COLOR__WHITE, 0, 0),
                                                   cli.WinString("Do you want to create new config file?",
                                                                 cli.COLOR__WHITE, 0,
                                                                 1)], )
        if create_new:
            extensions = select_config_folder_types()
            create_config_file(extensions)
        else:
            return
    elif config_file_state == ValidateConfigStatus.WRONG_STRUCTURE:
        question = [cli.WinString("Config file has invalid structure. These errors occurred:", cli.COLOR__WHITE, 0,
                                  0), ] + \
                   [cli.WinString(err_msg[i].value, cli.COLOR__RED, 0, i + 1) for i in range(len(err_msg))] + \
                   [cli.WinString("Do you want to create new config file or fix it by yourself?", cli.COLOR__WHITE, 0,
                                  len(err_msg) + 1)]
        rewrite_config = cli.CliUtils.yes_no(question=question, yes_string="Create new config file",
                                             no_string="I'll fix it by myself")
        if rewrite_config:
            extensions = select_config_folder_types()
            create_config_file(extensions)
        else:
            return

    run_folder_admin(verbose=True)


def validate_config_file() -> Tuple[List[ValidateConfigErrorMessage], ValidateConfigStatus]:
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


def select_config_folder_types() -> List[Extensions]:
    controller = cli.CLI()
    options = [cli.SelectOption(f'{str(extension.name).lower()}:({",".join(extension.value[:5])},...)', extension) for
               extension in Extensions]
    helper_text = [
        cli.WinString("Select types you want to organize in your folder:", cli.COLOR__WHITE, 0, 0),
        cli.WinString("Press 'space' to add/remove selection and 'enter' to confirm your selection:", cli.COLOR__WHITE,
                      0, 1),
    ]
    config = cli.SelectConfig(
        options=options,
        helper_text=helper_text,
        default_color=cli.COLOR__WHITE,
        highlighted_color=cli.COLOR__CYAN,
        start_x=0,
        start_y=2,
    )
    extensions = [option.value for option in controller.multi_select(config)]
    controller.exit()
    return extensions


def create_config_file(extensions: List[Extensions]) -> None:
    config_file_content = []
    for extension in extensions:
        config_file_content.append({"dirname": extension.name.lower(), "extensions": list(extension.value)})

    with open("FolderAdministratorConfig.json", "w") as config_file:
        json.dump(config_file_content, config_file, indent=4)


def run_folder_admin(verbose: bool = False):
    admin = FolderAdministrator(verbose)
    admin.move_files_to_dirs()


# executor for debug purposes
if __name__ == "__main__":
    main()
