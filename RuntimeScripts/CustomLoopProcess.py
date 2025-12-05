import pg_extended as pgx
from DBManagers.DBScripts.DBProtocols import DBProtocols
from DBManagers.DBScripts.InternalUpdates import InternalUpdates
from RuntimeScripts.FirstUpdate import firstUpdate
import sharedAssets

def customLoopProcess():
  window: pgx.Window = sharedAssets.app

  if window.firstUpdate:
    firstUpdateStatus = firstUpdate()

    if not firstUpdateStatus:
      Exception('You fucked up bad...')

  if DBProtocols.dbEventCheck('DBUpdate'):
    print('Updating Internal Database...')
    InternalUpdates.updateInternalDB()

    if 'GCList' in window.customData:
      InternalUpdates.updateGCList()

    print('Internal Database Updated Successfully')
