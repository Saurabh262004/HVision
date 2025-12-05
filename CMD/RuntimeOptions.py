from DBManagers.DBScripts.DBProtocols import DBProtocols

optionsDict = {}

def help():
  print('\n ----- HVision ----- \n')

  for k, v in optionsDict.items():
    print(f'{k}: {v['disc']}')

  print('\n')

def setupRuntimeOptions():
  optionsDict['help'] = {'fn': help, 'disc': 'Print this output.'}
  optionsDict['updateDB'] = {'fn': DBProtocols.generateDB, 'disc': 'Force update the database.'}
  optionsDict['verifyDB'] = {'fn': DBProtocols.verifyDB, 'disc': 'Verfies the database.'}
  optionsDict['verifyDBBackground'] = {'fn': DBProtocols.verifyDBBackground, 'disc': 'Verifies the database in a separate thread.'}

setupRuntimeOptions()
