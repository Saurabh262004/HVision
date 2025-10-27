import sharedAssets
import pg_extended as pgx
from RuntimeScripts.FirstUpdate import firstUpdate

def customLoopProcess():
  window: pgx.Window = sharedAssets.app

  if window.firstUpdate:
    firstUpdate()
