from DBManagers.DBScripts.DBProtocols import DBProtocols
from DBManagers.DBProcessors import ImageDBManager

optionsDict = {}

def help():
	print('\n ----- HVision ----- \n')

	for k, v in optionsDict.items():
		print(f'{k:<25}: {v['desc']}')

	print('')

def setupRuntimeOptions():
	optionsDict['help'] = {'fn': help, 'desc': 'Print this output.'}
	optionsDict['updateDB'] = {'fn': DBProtocols.generateDB, 'desc': 'Force update the database.'}
	optionsDict['refreshDB'] = {'fn': DBProtocols.refreshDB, 'desc': 'Generates new database, loads them, refreshes images database.'}
	optionsDict['verifyDB'] = {'fn': DBProtocols.verifyDB, 'desc': 'Verifies the database.'}
	optionsDict['verifyDBBackground'] = {'fn': DBProtocols.verifyDBBackground, 'desc': 'Verifies the database in a separate thread.'}
	optionsDict['loadDB'] = {'fn': DBProtocols.loadDB, 'desc': 'Loads the database file into `SharedAssets.db`'}
	optionsDict['loadOldDB'] = {'fn': DBProtocols.loadOldDB, 'desc': 'Loads the old database file into `SharedAssets.oldDB`'}
	optionsDict['updateImageDB'] = {'fn': ImageDBManager.updateImageDB, 'desc': 'Downloads new and updated images'}

setupRuntimeOptions()
