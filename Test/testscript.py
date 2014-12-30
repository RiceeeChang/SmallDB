import sys
import os

# change execute shell path
os.chdir(os.getcwd() + '/../')
sys.path.append(os.getcwd())


print(sys.path)
print(os.getcwd())

from SqlYacc import parser
import json
with open('Test/testsuit.json', 'r+') as datafile:
	testsuit = json.load(datafile)
	#print(testsuit)
	for testcase in testsuit:
		result = parser.parse(testcase['testcase'])
		if result['response'] == testcase['oracle']:
			print("ID: ", testcase['ID'], " resutl: Pass") # , ' testcase: ', testcase['testcase'])
		else:
			print("ID: ", testcase['ID'], " resutl: Fail")
			print('---- Testcase: ', testcase['testcase'])
			print('---- Error_Msg: ', result['response'])