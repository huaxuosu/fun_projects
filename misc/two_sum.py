inpLs = [1, 2, 3, 5, 11, 13, 25]
target = 16

# all numbers are unique in inpLs
def twoSum(inpLs, target):
    seen = {}
    for i in range(len(inpLs)):
        n = inpLs[i]
        comp = target - n
        if comp in seen:
            print(seen[comp], i)
        seen[n] = i
