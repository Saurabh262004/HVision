import pg_extended as pgx
import sharedAssets
from RuntimeScripts import customLoopProcess, closingSeq
from UI.Systems.Home import addHome

app = sharedAssets.app = pgx.Window('HVision', (1280, 720), customLoopProcess=customLoopProcess)

addHome()

app.openWindow()

closingSeq()
