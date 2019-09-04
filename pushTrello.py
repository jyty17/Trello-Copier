#!/usr/bin/env python3
import json, requests
import tokens_personal as tokens

# Before running program install the requests library using `pip install requests`
url = {
	"list": "https://api.trello.com/1/lists",
	"card": "https://api.trello.com/1/cards",
	"board": "https://api.trello.com/1/boards"
}
# Use this when no json data of old board exists
# response = requests.request("GET",
# 	url=url['board']+'/'+tokens.old_board_id,
# 	params={"key": tokens.key, "token": tokens.trello_token}
# )
# parse_json = json.loads(response.text)
with open('SleepawayTrello.json', 'r') as parsed:
	parse_json = json.load(parsed)
if parse_json:
	print("-----Parsed Json Successfully!")

boardIds = [l['id'] for l in parse_json['lists']]
boardNames = [l['name'] for l in parse_json['lists']]
boardPos = [l['pos'] for l in parse_json['lists']]
boardDict = dict(zip(boardIds, boardNames))

# Creates new lists based on jsons files
for i in zip(boardIds, boardNames, boardPos):
	params = {
		"name": i[1],
		"idBoard": tokens.board_id,
		"pos": i[2],
		"key": tokens.key,
		"token": tokens.trello_token
		}
	response = requests.request("POST", url=url["list"], params=params)
	if response.status_code == 200:
		print("List: {} ----- Successfully Created List {}".format(i[1], response.status_code))
	else:
		print("List: {} ----- Failed To Create List {}".format(i[1]))

response = requests.request("GET",
	url=url['board']+"/"+tokens.board_id+'/lists',
	params={"key": tokens.key, "token": tokens.trello_token}
)
if response.status_code == 200:
	newBoardLists = json.loads(response.text)
	newListIds = [(l['id'], l['name']) for l in newBoardLists]
	for card in parse_json['cards']:
		print('-----Parsing {}'.format(card['name']))
		for listId in newListIds:
			if boardDict[card['idList']] == listId[1]:
				params = {
					"idList": listId[0],
					"name": card['name'],
					"desc": card['desc'],
					'pos': card['pos'],
					"key": tokens.key,
					"token": tokens.trello_token
				}
				response=requests.request("POST", url=url['card'], params=params)
				if response.status_code == 200:
					print("Card: {} ----- Successfully Create Card {}".format(card['name'], response.status_code))
				else:
					print("Card: {} ----- Failed To Create Card {}".format(card['name'], response.status_code))
				# print(response.text)