queue = [1,2,3,4,5,5,5,8,9]

item = 6
search = item
minimum = 0
maximum = len(queue)-1
current = maximum//2

while queue[current] != search and minimum != maximum:
    if queue[current] < search:
        minimum = min(current + 1, maximum)
    elif queue[current] > search:
        maximum = max(current - 1, minimum)
    current = (minimum + maximum)//2
    print(minimum, current, maximum)
if queue[current] == search:
    while search == queue[current-1] and current > 0:
        current -= 1
    queue.insert(current,'a')

else:
    if search < queue[current]:
        queue.insert(current,'a')
    elif search > queue[current]:
        queue.insert(current+1,'a')

print(queue)
