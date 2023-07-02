# ToonBoom Incremental Save Installation Instructions

Make a folder called `packages` in your user scripts folder and copy `IncrementalSave` to it. This extension requires Python, so make sure that you have python 3.9+ installed on your system. If ToonBoom is having trouble finding your python install, try reinstalling python and making sure that you tell the installer to install for all users (you may have to do a custom install in order to do this).

Currently this only works on Windows because of the way it copies files in the `copy_files` method. Everything else should work on any platform, so if you want to get this working on a Mac that should be the only thing you need to change.