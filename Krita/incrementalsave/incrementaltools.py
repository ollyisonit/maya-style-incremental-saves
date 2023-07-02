import pathlib, re, shutil, subprocess
from typing import Callable


def increment(
    FILE_SUFFIX: str,
    get_project_path: Callable[[], str],
    save_project: Callable[[], None],
    save_project_as: Callable[[str], None],
    log_message: Callable[[str], None],
):
    """Runs an incremental save using the given parameters.
    :param FILE_SUFFIX: The file extension that identifies a project file. For instance, Nuke files are '.nk'. Pass an empty string if the project type has no extension.
    :param get_project_path: Method that get the full path to the project that you're saving, including the name of the project itself (ie. C:/Documents/project.nk)
    :param save_project: Method that saves project using application's API
    :param save_project_as: Method that saves project using the given name.
    :param log_message: Logs message to application console.
    """

    PROJECTNAME_PATTERN = r".*\.(\d*)" + FILE_SUFFIX + "$"
    FOLDER_PATTERN = (
        r".*/incrementalSaves/(?P<orig_name>.*)"
        + FILE_SUFFIX
        + r"/(?P=orig_name).(?P<number>\d*)"
        + FILE_SUFFIX
        + "$"
    )

    def copy_files(src, dst):
        shutil.copy2(src, dst)
        # subprocess.run(["robocopy", src, dst, "/mt", "/e"])

    def swap_increment():
        log_message("Checking whether this version is an increment...")
        comp_path = pathlib.Path(get_project_path())
        regex = FOLDER_PATTERN
        log_message(comp_path.as_posix())
        template_match = re.match(regex, comp_path.as_posix())
        if template_match is None:
            log_message("File does not follow formatting of an existing increment.")
            return False

        original_name = template_match.groupdict()["orig_name"]
        original_dir = comp_path
        while original_dir.name != "incrementalSaves":
            original_dir = original_dir.parent
        original_dir = original_dir.parent

        original_file = original_dir.joinpath(original_name).with_suffix(FILE_SUFFIX)

        if not original_file.exists():
            log_message(
                "File follows path of existing increment, but cannot find original"
                f" file at {original_file}"
            )
            return False

        next_increment = get_increment_level(comp_path.parent) + 1
        new_file = comp_path.parent.joinpath(
            f"{original_name}.{str(next_increment).rjust(4, '0')}{FILE_SUFFIX}"
        )
        log_message(
            "This file is a valid increment of an existing file. Copying original file"
            f" to {new_file}..."
        )
        shutil.move(original_file, new_file)
        log_message(f"Replacing original file with this one...")
        save_project_as(original_file.as_posix())
        log_message("This file is now the current version.")
        return True

    def get_increment_level(incrementalSavesPath):
        current_increment = -1
        for save in incrementalSavesPath.glob("*"):
            regex = PROJECTNAME_PATTERN
            number_match = re.match(regex, save.name)
            if number_match != None:
                number = number_match.groups()[0]
                if number != None:
                    number = int(number)
                    if number > current_increment:
                        current_increment = number
        return current_increment

    def increment_advance():
        log_message("Performing incremental save...")
        comp_path = pathlib.Path(get_project_path())
        log_message(f"Working with file: {comp_path}")
        comp_dir = comp_path.parent
        comp_name = comp_path.name
        comp_ext = comp_path.suffix
        log_message(comp_name)

        incrementalSavesPath = comp_dir.joinpath("incrementalSaves").joinpath(comp_name)

        if not incrementalSavesPath.exists():
            log_message(
                f"Incremental save path {incrementalSavesPath} does not exist,"
                " creating..."
            )
            incrementalSavesPath.mkdir(parents=True)

        log_message(f"Using incremental saves directory {incrementalSavesPath}")

        current_increment = get_increment_level(incrementalSavesPath) + 1

        incremented_file = incrementalSavesPath.joinpath(
            f"{comp_path.stem}.{str(current_increment).rjust(4, '0')}{comp_ext}"
        )

        log_message(f"Saving increment {incremented_file}...")

        copy_files(comp_path, incremented_file)

        log_message(f"Saving current version...")

        save_project()

    # Run increment operation using the functions defined above
    if not swap_increment():
        increment_advance()
    log_message("Incremental save complete!")
