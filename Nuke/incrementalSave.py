import nuke, pathlib, re, shutil, glob

def swap_increment():
    print("Checking whether this version is an increment...")
    comp_path = pathlib.Path(nuke.scriptName())
    regex = r'.*/incrementalSaves/(?P<orig_name>.*)\.nk/(?P=orig_name).(?P<number>\d*).nk$'
    print(comp_path.as_posix())
    template_match = re.match(regex, comp_path.as_posix())
    if template_match is None:
        print("File does not follow formatting of an existing increment.")
        return False
    
    original_name = template_match.groupdict()['orig_name']
    original_dir = comp_path
    while original_dir.name is not 'incrementalSaves':
        original_dir = original_dir.parent
    original_dir = original_dir.parent

    original_file = original_dir.joinpath(original_name).with_suffix('.nk')

    if not original_file.exists():
        print(f"File follows path of existing increment, but cannot find original file at {original_file}")
        return False
    
    next_increment = get_increment_level(comp_path.parent) + 1
    new_file = comp_path.parent.joinpath(f"{original_name}.{str(next_increment).rjust(4, '0')}.nk")
    print(f"This file is a valid increment of an existing file. Copying original file to {new_file}...")
    shutil.copy(original_file, new_file)
    print(f"Replacing original file with this one...")
    nuke.scriptSaveAs(filename=original_file.as_posix(), overwrite=True)
    print("This file is now the current version.")
    return True

def increment():
    if not swap_increment():
        increment_advance()

def get_increment_level(incrementalSavesPath):
    current_increment = -1
    for save in incrementalSavesPath.glob("*"):
        regex = r".*\.(\d*)\.nk$"
        number_match = re.match(regex, save.name)
        if number_match is not None:
            number = number_match.groups()[0]
            if number != None:
                number = int(number)
                if number > current_increment:
                    current_increment = number
    return current_increment

def increment_advance():
    print("Performing incremental save...")
    comp_path = pathlib.Path(nuke.scriptName())
    print(f"Working with file: {comp_path}")
    comp_dir = comp_path.parent
    comp_name = comp_path.name
    comp_ext = comp_path.suffix
    print(comp_name)

    incrementalSavesPath = comp_dir.joinpath("incrementalSaves").joinpath(comp_name)

    if not incrementalSavesPath.exists():
        print(f"Incremental save path {incrementalSavesPath} does not exist, creating...")
        incrementalSavesPath.mkdir(parents=True)

    print(f"Using incremental saves directory {incrementalSavesPath}")

    current_increment = get_increment_level(incrementalSavesPath) + 1

    incremented_file = incrementalSavesPath.joinpath(f"{comp_path.stem}.{str(current_increment).rjust(4, '0')}{comp_ext}")

    print(f"Saving increment {incremented_file}...")

    shutil.copy(comp_path, incremented_file)

    print(f"Saving current version...")

    nuke.scriptSave()


