import pg_extended as pgx
import sharedAssets
from UI import addHome

app = sharedAssets.app = pgx.Window('HVision', (1280, 720))

addHome(app)

app.activateSystems('homeSystem')

app.openWindow()
