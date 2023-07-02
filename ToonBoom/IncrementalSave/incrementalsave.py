import pathlib, re, shutil, subprocess
from ToonBoom import harmony

current_session = harmony.session()

# like ".nk"
FILE_SUFFIX = ""
PROJECTNAME_PATTERN = r".*\.(\d*)" + FILE_SUFFIX + "$"
FOLDER_PATTERN = (
    r".*/incrementalSaves/(?P<orig_name>.*)/(?P=orig_name).(?P<number>\d*)"
    + FILE_SUFFIX
    + "$"
)


def get_project_path():
    return current_session.project.project_path


def save_project():
    current_session.project.save_all()


def save_project_as(name):
    current_session.project.save_as(name)


def copy_files(src, dst):
    subprocess.run(["robocopy", src, dst, "/mt", "/e"])


def increment():
    if not swap_increment():
        increment_advance()
    current_session.log("Incremental save complete!")


def swap_increment():
    current_session.log("Checking whether this version is an increment...")
    comp_path = pathlib.Path(get_project_path())
    regex = FOLDER_PATTERN
    current_session.log(comp_path.as_posix())
    template_match = re.match(regex, comp_path.as_posix())
    if template_match is None:
        current_session.log("File does not follow formatting of an existing increment.")
        return False

    original_name = template_match.groupdict()["orig_name"]
    original_dir = comp_path
    while original_dir.name != "incrementalSaves":
        original_dir = original_dir.parent
    original_dir = original_dir.parent

    original_file = original_dir.joinpath(original_name).with_suffix(FILE_SUFFIX)

    if not original_file.exists():
        current_session.log(
            f"File follows path of existing increment, but cannot find original file at {original_file}"
        )
        return False

    next_increment = get_increment_level(comp_path.parent) + 1
    new_file = comp_path.parent.joinpath(
        f"{original_name}.{str(next_increment).rjust(4, '0')}{FILE_SUFFIX}"
    )
    current_session.log(
        f"This file is a valid increment of an existing file. Copying original file to {new_file}..."
    )
    shutil.move(original_file, new_file)
    current_session.log(f"Replacing original file with this one...")
    save_project_as(original_file.as_posix())
    current_session.log("This file is now the current version.")
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
    current_session.log("Performing incremental save...")
    comp_path = pathlib.Path(get_project_path())
    current_session.log(f"Working with file: {comp_path}")
    comp_dir = comp_path.parent
    comp_name = comp_path.name
    comp_ext = comp_path.suffix
    current_session.log(comp_name)

    incrementalSavesPath = comp_dir.joinpath("incrementalSaves").joinpath(comp_name)

    if not incrementalSavesPath.exists():
        current_session.log(
            f"Incremental save path {incrementalSavesPath} does not exist, creating..."
        )
        incrementalSavesPath.mkdir(parents=True)

    current_session.log(f"Using incremental saves directory {incrementalSavesPath}")

    current_increment = get_increment_level(incrementalSavesPath) + 1

    incremented_file = incrementalSavesPath.joinpath(
        f"{comp_path.stem}.{str(current_increment).rjust(4, '0')}{comp_ext}"
    )

    current_session.log(f"Saving increment {incremented_file}...")

    copy_files(comp_path, incremented_file)

    current_session.log(f"Saving current version...")

    save_project()
