# Nuke Incremental Save Installation Instructions

Copy `incrementalSave.py` to your `.nuke` folder. Add `import incrementalSave` to `init.py` to import the script on launch, and add `nuke.menu('Nuke').addCommand('File/Incremental Save', 'incrementalSave.increment()', 'Ctrl+S')` to `menu.py` to add it to the menu. This will also make it so that `Ctrl + S` runs an incremental save instead of a normal save--if you don't want that behavior, change the hotkey in the `menu.py` command to something else.

