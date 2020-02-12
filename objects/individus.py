class Individu:
    def __init__(self, ID, pere, mere, sequence):
        self.ID = ID
        self.pere = pere
        self.mere = mere
        self.sequence = sequence
        self.cout = "N/A"

    def __str__(self):
        if type(self.pere)==str:
            return 'ID: {}, Pere: {}, Mere: {}, Cout: {}'.format(self.ID, "Adam", "Eve", self.cout)
        else:
            return 'ID: {}, Pere: {}, Mere: {}, Cout: {}'.format(self.ID, self.pere.ID, self.mere.ID, self.cout)

    def set_cout(self, cout):
        self.cout = cout