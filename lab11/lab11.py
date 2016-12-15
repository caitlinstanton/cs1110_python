def numberof(seq,v):
	length = 0
	count = 0
	while length < len(seq):
		if seq[length] == v:
			count = count + 1
		length = length + 1
	return count

seq = [1, 3, 4, 5, 5, 5]
print numberof(seq,5)

def replace_copy(seq, a, b):
	length = 0
	result = []
	while length < len(seq):
		if seq[length] == a:
			print "a"
			result.append(b)
		else:
			result.append(seq[length])
		length = length + 1
	return result

print replace_copy(seq,5,7)
