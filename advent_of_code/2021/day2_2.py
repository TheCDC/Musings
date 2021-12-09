with open('inputs/day2.txt') as f:
    lines = f.read().strip().split('\n')
    commands = [l.split() for l in lines]
position = {'x': 0, 'y': 0,'aim':0}
for index,c in enumerate( commands):
    num = int(c[1])
    name = c[0]
    match name:
        case 'forward':
            position['x'] += num
            position['y'] += position['aim']*num
        case 'up':
            position['aim'] -= num  
        case 'down':
            position['aim'] += num
print(position,position['x']*position['y'])

