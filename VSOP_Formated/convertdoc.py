f = file('/home/owner/Desktop/TCS_code/VSOP/VSOP87B.sat', 'r')

for line in f:
	arr = line.split()
	if len(arr) > 0:
		if arr[0] == 'VSOP87':
			print line
		else:
			print arr[-3], arr[-2], arr[-1]
