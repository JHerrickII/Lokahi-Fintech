wordOne = list(input("Enter a word to compare: "))
wordTwo = list(input("Enter a second word to compare to the first: "))
if len(wordOne) != len(wordTwo): 
	print ("This is not a permutation of " + wordOne)

for i in range(0,len(wordOne)): #both equal so does not matter
	j=0
	k= False
	while j < len(wordTwo) and k == False:
		if wordOne[i] == wordTwo[j]:
			k=True
			del wordTwo[j]
		else:
			j+=1

if len(wordTwo) == 0:
	print("This was a permutation of " + "".join(wordOne))
else:
	print("This was not a permutation of " + "".join(wordOne))

#improvements: 
#could do this with hashmap with key/value be letter/frequency, then check if same table created (Subtraction? )