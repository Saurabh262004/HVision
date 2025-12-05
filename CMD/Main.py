from CMD.RuntimeOptions import optionsDict

def TUI():
  running=True

  tuiInput = ''

  while running:

    tuiInput = input('HVision: ')

    if tuiInput in optionsDict:
      optionsDict[tuiInput]['fn']()

    elif tuiInput == 'quit' or tuiInput == 'q':
      print('Quitting HVision')
      running = False

    else:
      print(f'[INFO] {tuiInput} is not a recgnised option')
