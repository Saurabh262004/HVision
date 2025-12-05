def TUI():
  running=True

  tuiInput = ''

  while running:

    tuiInput = input().lower()

    if tuiInput == 'quit' or tuiInput == 'q':
      running = False
