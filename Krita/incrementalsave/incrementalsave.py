# type: ignore
from krita import *
from functools import partial
from . import incrementaltools


class IncrementalSaveExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def incremental_save(self):
        if Krita.instance().activeDocument().fileName() == "":
            Krita.instance().action("file_save_as").trigger()
        else:
            incrementaltools.increment(
                ".kra",
                Krita.instance().activeDocument().fileName,
                Krita.instance().activeDocument().save,
                Krita.instance().activeDocument().saveAs,
                lambda msg: print(msg),
            )

    def setup(self):
        pass

    def createActions(self, window):
        incremental_save_action = window.createAction(
            "dninosores.incrementalsave", "Incremental Save", "file"
        )
        incremental_save_action.triggered.connect(self.incremental_save)
        QTimer.singleShot(
            0,
            partial(
                self.moveAction,
                incremental_save_action,
                "file_save_as",
                "file",
                window.qwindow(),
            ),
        )

    # Take the existing export_region action and move it to be after file_export in the file menu
    def moveAction(self, action, preceeding_name, menu_title, qwindow):
        menu_bar = qwindow.menuBar()
        file_menu_action = next(
            (a for a in menu_bar.actions() if a.objectName() == menu_title), None
        )
        if file_menu_action:
            file_menu = file_menu_action.menu()
            # insertAction will place the new entry above the given action,
            # so we need to continue for one more iteration before inserting
            found_item = False
            for file_action in file_menu.actions():
                if found_item:
                    file_menu.removeAction(action)
                    file_menu.insertAction(file_action, action)
                    break
                if file_action.objectName() == preceeding_name:
                    found_item = True


Krita.instance().addExtension(IncrementalSaveExtension(Krita.instance()))
