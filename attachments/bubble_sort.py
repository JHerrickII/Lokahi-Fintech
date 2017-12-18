def bubbleSort(sortList):
	sorted = False
	while not sorted:
		sorted=True #sets equal to true
		for i in range (0,len(sortList)-1):
			if sortList[i] > sortList[i+1]:
				temp = sortList[i]
				sortList[i] = sortList[i+1]
				sortList[i+1] = temp
				sorted = False #only if entire list sorted now

	return sortList

unsortedList = [2,3,1,5,7,4,3,9,1]
print(bubbleSort(unsortedList))
