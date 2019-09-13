def get_info(file):
	try:
		"""
		0|Flamingo #name
		1|Kero Kero Bonito #name
		2|89 #bpm
		3|1489 #note
		4|1500 #length
		difficulty: ~2 easy 3~5 medium 6~ hard
		"""
		infolist = file.read().split("\n")
		notepermin = int(infolist[3]) / (int(infolist[4]) / 60)
		if notepermin < 3:
			difficulty = "EASY"
		elif 3 < notepermin < 6:
			difficulty = "MEDIUM"
		elif 6 < notepermin < 10:
			difficulty = "HARD"
		elif 10 < notepermin:
			difficulty = "EXTREME"
		return (infolist[0], infolist[1], infolist[2], infolist[3], infolist[4], difficulty)
	#return value : name,		artist,		BPM,	   note amount,	song length, difficulty
	except Exception as e:
		return (1, "0of! looks like your info file is written by a n00b!\nError Message:"+e)
def get_note(file):
	try:
		notelist =  file.read().split("\n")
		rtnlist = [[], [], [], [], [], []]
		ver = notelist[0][4:]
		if ver == "A3":
			tmp = 0
			for x in notelist[2:]:
				if x == "/":
					tmp += 1
				else:
					rtnlist[tmp].append(x)
		elif ver == "A4":
			bpm = 0
			div = 0
			time = 0
			for x in notelist[1:]:
				if x[0] == "b":
					bpm = int(x[1:])
				elif x[0] == "d":
					div = int(x[1:])
				elif x[0] == "w":
					time = int(x[1:])
				elif x[0] == "/":
					time += ((60 / bpm) / div) * int(x[1:])
				else:
					for y in x:
						rtnlist[int(y)].append(time)
					time += (60 / bpm) / div
		return rtnlist
	except Exception as e:
		return (1, "Yeouch! There is a wild exception in the note file!\nError Message: "+e)
