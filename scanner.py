"""
Sample script to test ad-hoc scanning by table drive.
This accepts "term","test" and "long" words.
"""
file = open("testfile.txt","a")
global found
found = 1
def getchar(words,pos):
	""" returns char at pos of words, or None if out of bounds """
	global found
	if pos<0 or pos>=len(words): return None
	if found == 1:
		file.write(words +"\n")
		found = 2
	return words[pos]


def scan(text,transition_table,accept_states):
	""" Scans `text` while transitions exist in 'transition_table'.
	After that, if in a state belonging to `accept_states`,
	returns the corresponding token, else ERROR_TOKEN.
	"""

	# initial state
	pos = 0
	state = 'q0'

	chars1 = ('.',':')
	while True:

		c = getchar(text,pos)	# get next char

		if state in transition_table and c in transition_table[state]:

			state = transition_table[state][c]	# set new state
			pos += 1	# advance to next char

		else:	# no transition found

			# check if current state is accepting
			if state in accept_states:
				return accept_states[state],pos

			# current state is not accepting
			print("ERROR_TOKEN")
			file.write("ERROR_TOKEN "+"\n")
			return 'ERROR_TOKEN',pos


# the transition table, as a dictionary
td = { 'q0':{ '0':'q1','1':'q1','2':'q3','3':'q2','4':'q2','5':'q2','6':'q2','7':'q2','8':'q2','9':'q2' },
       'q1':{ '1':'q2','2':'q2','3':'q2','4':'q2','0':'q2','5':'q2','6':'q2','7':'q2','8':'q2','9':'q2','.':'q4',':':'q4' },
       'q2':{ '.':'q4',':':'q4' },
	   'q3':{ '0':'q2','1':'q2','2':'q2','3':'q2','.':'q4',':':'q4'},
	   'q4':{ '0':'q5','1':'q5','2':'q5','3':'q5','4':'q5','5':'q5' },
	   'q5':{ '1':'q6','2':'q6','3':'q6','4':'q6','5':'q6','6':'q6','7':'q6','8':'q6','9':'q6','0':'q6' }
	 
     }

# the dictionary of accepting states and their
# corresponding token
ad = { 'q6':'TIME_TOKEN',
       'q7':'TERM_TOKEN',
       'q10':'LONG_TOKEN'
     }


# get a string from input
text = input('give some input>')
file.write("give some input> "+"\n")
# scan text until no more input
while text:	# that is, while len(text)>0

	# get next token and position after last char recognized
	token,position = scan(text,td,ad)

	if token=='ERROR_TOKEN':
		print('unrecognized input at pos',position+1,'of',text)
		wut = str(position+1)
		file.write('unrecognized input at pos '+wut+' of'+text+"\n\n")
		break

	print("token:",token,"string:",text[:position])
	file.write("token: "+token+"string: "+text[:position]+"\n\n")
	# remaining text for next scan
	text = text[position:]
