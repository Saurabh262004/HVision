from CMD import getArgs
import SharedAssets

def bootGUI():
  print('Running in GUI mode')

  import pg_extended as pgx
  from RuntimeScripts import customLoopProcess, closingSeq

  app = SharedAssets.app = pgx.Window('HVision', (1280, 720), customLoopProcess=customLoopProcess)

  app.openWindow()

  closingSeq()

def bootTUI():
  print('Running in TUI mode.')

  from CMD import TUI

  TUI()

def main():
  args = SharedAssets.args = getArgs()

  if args.force_update_db:
    print('Force updating database')

    from DBManagers.DBScripts.DBProtocols import DBProtocols
    DBProtocols.generateDB()

  if args.no_gui:
    bootTUI()

  else:
    bootGUI()

if __name__ == '__main__':
  main()
