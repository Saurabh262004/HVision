from DBManagers.DBScripts.DBProtocols import DBProtocols

optionsDict = {}

def help():
  print('\n ----- HVision ----- \n')

  for k, v in optionsDict.items():
    print(f'{k:<25}: {v['desc']}')

  print('')

def setupRuntimeOptions():
  optionsDict['help'] = {'fn': help, 'desc': 'Print this output.'}
  optionsDict['updateDB'] = {'fn': DBProtocols.generateDB, 'desc': 'Force update the database.'}
  optionsDict['verifyDB'] = {'fn': DBProtocols.verifyDB, 'desc': 'Verifies the database.'}
  optionsDict['verifyDBBackground'] = {'fn': DBProtocols.verifyDBBackground, 'desc': 'Verifies the database in a separate thread.'}

setupRuntimeOptions()
