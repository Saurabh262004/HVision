import pg_extended as pgx
import sharedAssets
from RuntimeScripts import customLoopProcess, closingSeq

def main():
  app = sharedAssets.app = pgx.Window('HVision', (1280, 720), customLoopProcess=customLoopProcess)

  app.openWindow()

  closingSeq()

if __name__ == '__main__':
  main()
