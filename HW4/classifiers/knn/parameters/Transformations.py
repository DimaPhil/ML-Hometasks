class Transformations:
    transformations = [
        lambda data: data,
        lambda data: [[element[0], element[1], (4 * element[0]**2 + 4 * element[1]**2), element[2]] for element in data]
    ]

    def __init__(self, id):
        self.transformation = self.transformations[id]

    def get(self, data):
        return self.transformation(data)

    @staticmethod
    def get_transformations(self):
        return self.transformations
