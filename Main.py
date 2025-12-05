from CMD import getArgs

def bootGUI():
  import pg_extended as pgx
  import SharedAssets
  from RuntimeScripts import customLoopProcess, closingSeq

  app = SharedAssets.app = pgx.Window('HVision', (1280, 720), customLoopProcess=customLoopProcess)

  app.openWindow()

  closingSeq()

def main():
  args = getArgs()

  if args.no_gui:
    print('Running in TUI mode.')
 
    from CMD import TUI
    TUI()
 
  else:
    print('Running in GUI mode')
 
    bootGUI()

if __name__ == '__main__':
  main()
