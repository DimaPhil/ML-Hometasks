def loadData(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            x, y, label = map(float, line.split(','))
            label = int(label)
            data.append([x, y, label])
    return data