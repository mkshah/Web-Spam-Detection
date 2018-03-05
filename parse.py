maxn = 114528
n = int(raw_input())
#text = [[0]*maxn]*10
text = []
for i in range(maxn):
	text.append([])
for i in range(maxn):
	for j in range(maxn):
		text[i].append(0)
#print(text)
for i in range(n):
	string = (raw_input()).split()
	for j in range(len(string)):
		listing = string[j].split(':')
		text[i][int(listing[0])] = int(listing[1])


for i in range(maxn):
	for j in range(maxn):
		print(text[i][j]),
		print(" "),
	print


		
