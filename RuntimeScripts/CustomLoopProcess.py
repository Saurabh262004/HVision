import os
import pg_extended as pgx
from RuntimeScripts.DBScripts.DBProtocols import DBProtocols
from RuntimeScripts.FirstUpdate import firstUpdate
import sharedAssets

def customLoopProcess():
  window: pgx.Window = sharedAssets.app

  if window.firstUpdate:
    firstUpdateStatus = firstUpdate()

    if not firstUpdateStatus:
      Exception('You fucked up bad...')

  if DBProtocols.dbEventCheck('DBUpdate'):
    DBProtocols.loadDB()
    DBProtocols.dbEventClose('DBUpdate')
