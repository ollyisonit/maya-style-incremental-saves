const ID_PREFIX = "com.dninosores";

const CATEGORY_NAME = "Dninosores TB Incremental Save";

function incrementalSave() {
  var python = PythonManager.createPyObject(
    specialFolders.userScripts + "/packages/TBIncrementalSave/incrementalsave.py");
  MessageLog.trace("SAVING")
  python.py.increment()
  scene.saveAll()
  MessageBox.information("Incremental save complete!")
}

function configure(packageFolder, packageName) {
  MessageLog.trace(
    "Package " +
      packageName +
      " configure was called in folder: " +
      packageFolder
  );

  var tbIncrementalSaveAction = {
    id: ID_PREFIX + ".tbIncrementalSaveAction",
    text: "Increment and Save",
    checkable: false,
    isEnabled: true,
    onTrigger: incrementalSave,
  };
  ScriptManager.addAction(tbIncrementalSaveAction);

  ScriptManager.addShortcut({
    id: tbIncrementalSaveAction.id,
    text: tbIncrementalSaveAction.text,
    longDesc:
      "Saves old version of project into incrementalSaves folder.",
    order: "256",
    responder: "ScriptManagerResponder",
    slot: "onTriggerScriptAction(QString)",
    itemParameter: tbIncrementalSaveAction.id,
    categoryId: CATEGORY_NAME,
    categoryText: CATEGORY_NAME,
  });

  ScriptManager.addMenuItem({
    targetMenuId: "File",
    id: tbIncrementalSaveAction.id,
    text: tbIncrementalSaveAction.text,
    action: tbIncrementalSaveAction.id
  });

}
exports.configure = configure;
