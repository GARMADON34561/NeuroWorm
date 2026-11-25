class Neuron:

    def __init__(self, threshold=5):
        self.threshold = threshold
        self.potential = 0

    def stimulate(self, amount=1):

        self.potential += amount

        print(
            f"Neuron potential = "
            f"{self.potential}"
        )

        if self.potential >= self.threshold:

            self.potential = 0

            print("NEURON FIRED")

            return True

        return False