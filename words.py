
# count lines, sentences, and words of a text file
def wordStructure(fileName):
	lines, blanklines, sentences, words, maxlen = 0, 0, 0, 0, 0
	allwords = []
	maxword = 0
	wordLength = 0
	avgWordLength = 0
	#print '-' * 80

	try:
		filename = fileName
		textf = open(filename, 'r')

	except IOError:
		print 'Cannot open file %s for reading' % filename
		import sys
		sys.exit(0)

	# reads one line at a time
	for line in textf:
		#print line, 
		lines += 1
		
		if line.startswith('\n'):
			blanklines += 1
		else:
			# Each sentence ends with . or ? or !
			sentences += line.count('.') + line.count('!') + line.count('?')
		
			tempwords = line.split(None)
			#print tempwords 
		
			allwords = allwords + tempwords

			words += len(tempwords)

	
	for word in allwords:
		wordLength += len(word)
		if len(word) > maxlen:
			maxlen = len(word)
			maxword = word
	
	avgWordLength = wordLength / words
	textf.close()

	#print '-' * 80
	#print "All words: ", allwords
	#print '-' * 80
	#print "Lines : ", lines
	#print "Blank Lines: ", blanklines
	#print "Sentences : ", sentences
	#print "Words : ", words
	#print "Max Len: ", maxlen
	#print "Max Len word: ", maxword
	#print "Total length: ", wordLength
	#print "Avg Length of word: ",avgWordLength
	return words, maxword, avgWordLength

# list of file names
#files = ['xyz.txt']
#files.append('abc.txt')
# list of len of file

#for fname in files:
	#print "*" * 80
	#length.append(wordStructure(fname))
#print length

length = []
maxwords = []
avgLength = []
import glob
for fname in glob.glob('*.txt'):
	#print fname
	#print '*' * 80
	no, largestWord, avg = wordStructure(fname)
	length.append(no)
	maxwords.append(largestWord)
	avgLength.append(avg)
print "Results: "
print length
print maxwords
print avgLength

print "Cross Checking Results: "
print len(length)
print len(avgLength)


