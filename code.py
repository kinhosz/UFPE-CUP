import json

def readHistory():
	f = open("data.json", "r")
	data = json.loads(f.read())
	f.close()

	return data

def getScore():
	score = [26, 18, 15, 12, 10, 8, 6, 4, 2, 1]

	return score

def sortCompare(e):
	return e['score']

def createRank(data):
	score = getScore()

	handles = {}

	for k in data.keys():
		current = data[k]

		position = 0
		for handle in current:
			if position >= len(score):
				scoring = 1
			else:
				scoring = score[position]

			if handle in handles.keys():
				handles[handle] = handles[handle] + scoring
			else:
				handles[handle] = scoring
			position = position + 1

	rank = []

	for h in handles.keys():
		r = {
			"handle": h,
			"score": handles[h],
			"position": -1,
			"delta": 0
		}
		rank.append(r)

	rank.sort(reverse=True, key=sortCompare)

	pos = 1
	for r in rank:
		r["position"] = pos
		pos = pos + 1

	return rank

def readNewRanking():
	f = open("add.in", "r")
	handles = f.read().split('\n')
	f.close()

	return handles

def updateData(general, update):
	nid = len(general)

	general[nid] = update

	f = open("data.json", "w")
	f.write(json.dumps(general))
	f.close()

def updateRank(history, update):

	handles = {}

	for i in range(len(history)):
		k = history[i]['handle']
		handles[k] = history[i]['score']

	score = getScore()

	handles = {}

	current = update

	position = 0
	for handle in current:
		if position >= len(score):
			scoring = 1
		else:
			scoring = score[position]

		if handle in handles.keys():
			handles[handle] = handles[handle] + scoring
		else:
			handles[handle] = scoring
		position = position + 1

	rank = []

	for h in handles.keys():
		r = {
			"handle": h,
			"score": handles[h],
			"delta": 0
		}
		rank.append(r)

	for h in history:
		found = False
		for r in rank:
			if r['handle'] == h['handle']:
				found = True

		if found == False:
			rank.append(h)

	rank.sort(reverse=True, key=sortCompare)

	pos = 1
	for r in rank:
		r["position"] = pos
		pos = pos + 1

	for r in rank:
		for h in history:
			if r['handle'] == h['handle']:
				r['delta'] = h['position'] - r['position']
				break

	return rank

def showRank(new_ranking):

	out = ""

	for r in new_ranking:
		out = out + str(r['position']) + ": "
		out = out + str(r['score']) + ' - '
		out = out + r['handle']
		out = out + "(" + str(r['delta']) + ")" + '\n'

	f = open("show.out", "w")
	f.write(out)
	f.close()

def main():
	data = readHistory()

	rank = createRank(data)

	current_rank = readNewRanking()

	updateData(data, current_rank)
	new_ranking = updateRank(rank, current_rank)
	showRank(new_ranking)

if __name__ == "__main__":
	main()