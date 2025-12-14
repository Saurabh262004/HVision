import argparse

def getArgs() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="TUI for HVision.")

  parser.add_argument(
    '--no-gui',
    '-ng',
    action='store_true',
    help='Run HVision in TUI (Text User Interface) mode without GUI'
  )

  parser.add_argument(
    '--force-update-db',
    '-fdb',
    action='store_true',
    help='Force update the database on startup'
  )

  parser.add_argument(
    '--no-update-db',
    '-ndb',
    action='store_true',
    help='Don\'t update db if one already exists'
  )

  return parser.parse_args()
