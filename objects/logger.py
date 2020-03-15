import hashlib


class Logger:
    def __init__(self, instance, heuristique, **attributes):
        self.heuristique = heuristique
        self.attributes = attributes
        for attr_name, attr_value in attributes.items():
            setattr(self, attr_name, attr_value)
        self.instance = instance
        self.nom = self._hashed() + str(".txt")
        self.location = "Results/" + self.instance.nom + '_' + self.nom
        self.file = self._createFile()

    def _createFile(self):
        file = open(self.location, 'w')
        file.write("Instance: ")
        file.write(self.instance.nom)
        file.write("\n")
        file.write("Heuristique: ")
        file.write(str(self.heuristique))
        file.write("\n")
        file.write("___________________________________________________________________")
        file.write("\n")
        file.write("========================== Paramètre(s): ==========================")
        file.write("\n")
        file.write("___________________________________________________________________")
        file.write("\n")
        for attr_name, attr_value in self.attributes.items():
            file.write(str(attr_name))
            file.write(": ")
            file.write(str(attr_value))
            file.write("\n")
        file.write("___________________________________________________________________")
        file.write("\n")
        file.write("============================== Logs ===============================")
        file.write("\n")
        file.write("___________________________________________________________________")
        file.write("\n")

        file.close()
        return file

    def addLine(self, texte):
        file = open(self.location, 'a')
        file.write(str(texte))
        file.write("\n")
        file.close()

    def makespanFile(self, makespan, best):
        with open(self.location, 'r') as file:
            lines = file.readlines()
            lines.insert(2, "\n")
            lines.insert(2, "MakeSpan: " + str(makespan))
            lines.insert(2, "\n")
            lines.insert(2, "Séquence finale: " + str(best))
        file = open(self.location, 'w')
        for line in lines:
            file.write(str(line))
        file.close

    def itFile(self, it):
        with open(self.location, 'r') as file:
            lines = file.readlines()
            lines.insert(2, "\n")
            lines.insert(2, "Itérations: " + str(it))
        file = open(self.location, 'w')
        for line in lines:
            file.write(str(line))
        file.close

    def tpsFile(self, temps, nom="Temps :"):
        with open(self.location, 'r') as file:
            lines = file.readlines()
            lines.insert(2, "\n")
            lines.insert(2, nom + str(round(temps, 2)))

        file = open(self.location, 'w')
        for line in lines:
            file.write(str(line))
        file.close

    def fitOverTIme(self, meanfit, maxfit, nom="Mean Fit :", nom2="Max Fit"):
        with open(self.location, 'r') as file:
            lines = file.readlines()
            lines.insert(2, "\n")
            lines.insert(2, nom + str(meanfit))
            lines.insert(2, "\n")
            lines.insert(2, nom2 + str(maxfit))
        file = open(self.location, 'w')
        for line in lines:
            file.write(str(line))
        file.close

    def _hashed(self):
        hash = hashlib.blake2s(str(self.instance.nom + str(self.attributes)).encode(),
                               key=b'AP', digest_size=4).hexdigest()
        return str(hash)
