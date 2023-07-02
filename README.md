# Maya-Style Incremental Save Plugins

Maya has a really neat feature called incremental save where as you save your project a version history will be saved in an adjacent folder called `incrementalSaves`. I've often found myself wishing that other applications would organize incremental saving the same way that Maya did, so I've decided to start implementing Maya-style incremental save system in other applications I use.

Each folder in this repository contains an incremental save script or plugin designed to add Maya-style incremental saves to another application, as well as instructions for how to install it. Feel free to fork and submit a PR if you want to add an application that isn't supported yet! Make sure to read through the Behavior and Implementation sections though, as the purpose of this repository is to make incremental save behave exactly the same across all applications it's implemented for.

### Behavior 

There are two main features in Maya's incremental save. The first is that if you save a file, its version history will be saved in an `incrementalSaves` folder in the same directory as `filename.####.ext`. However, if you open a file in the version history and save it, then the file you saved will become the new current version. Here's an example:

Let's say you have a file called `test.ma`. If you save the file, the original `test.ma` will be copied to `incrementalSaves/test.0000.ma` and then the new version of the file will be saved as `test.ma`. Each time `test.ma` is saved, a new version is copied to `incrementalSaves`. 

Now let's say that you have three incremental saves: `test.0001.ma`, `test.0002.ma`, and `test.0003.ma`. If you open `test.0002.ma` and then save it, the original `test.ma` will be copied to `test.0004.ma` and the file you saved will become the new `test.ma`. Saving an incremented file is like rolling back to an older version.

This is what the directory structure would look like:

```
- test.ma
- incrementalSaves
	| - test.0001.ma
	| - test.0002.ma
	| - test.0003.ma
	| - test.0004.ma
```





### Implementation

Here's the algorithm that I use for incremental saving. These steps should run when the incremental save operation is run:

1. Check whether the currently opened file is an incremental save of a different file. If the current file has a name of the form `NAME.####.ext`, is saved in a directory called `incrementalSaves`, and a file called `NAME.ext` exists in the parent directory, then the current file is an incremental save.
2. If the currently opened file is not an incremental save, copy the file to `incrementalSaves/NAME.####.ext`. Figure out the number to use by scanning the `incrementalSaves` directory and finding the highest current increment number, then adding one. If `incrementalSaves` doesn't exist, create the directory and copy the file as `NAME.0000.ext`. Once the old version is copied, run File > Save (or equivalent) to save the new version of the file as `NAME.ext`
3. If the currently opened file is an incremental save, copy the original file (`NAME.ext`) to the `incrementalSaves` folder using the same process as step 2, then save the currently opened file as `NAME.ext`. 