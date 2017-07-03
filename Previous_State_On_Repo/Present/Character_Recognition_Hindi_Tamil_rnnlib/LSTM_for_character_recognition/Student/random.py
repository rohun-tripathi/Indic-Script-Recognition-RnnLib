
f = open("randomtrial")
count =0
for n in  f.readlines():
	if n == "\n":
		print "found"
		count += 1
	print n, "check"
	if n == '':
		print "Jaackpot"
print "Count == ", count