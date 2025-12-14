from DBManagers.DBScripts.DBProtocols import DBProtocols
from UI.SetupSystems import setupSystems
import SharedAssets

# implement error messages in the future
def firstUpdate() -> bool | None:
  loadDBSuccess = DBProtocols.loadDB()

  # can't proceed if we don't have the DB. User will have to wait till it's generated
  if not loadDBSuccess:
    print('failed to load db, generating a new one...')
    if not DBProtocols.verifyDB():
      return False
  else:
    if not SharedAssets.args.no_update_db:
      # if we do have the db, proceed and have a different process varify and update it if needed
      print('varifying db in background')
      DBProtocols.verifyDBBackground()
    else:
      print('Database is loaded successfully but won\'t be updated')

  setupSystems()

  SharedAssets.app.customData['triggerOPIntroFunc']()

  return True
