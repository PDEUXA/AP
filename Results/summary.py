import argparse
import hashlib
import os
import sys


def main(agrs):
    """
    Résume les intances contenu dans un dossier
    :param args: String, chemin du dossier
    :return:
    """

    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--chemin",
        type=str,
        help="Chemin du dossier.", )
    args = parser.parse_args()

    hash = hashlib.blake2s(str(args.chemin).encode(), key=b'AP', digest_size=2).hexdigest()

    makespan = []
    temps = []
    compt = 0
    for file in os.listdir(args.chemin):
        with open(args.chemin + '/' + file, "r") as f:
            for line in f.readlines():
                if "MakeSpan" in line:
                    makespan.append(int(line.split()[1]))
                if "Optimum trouvé au bout de: " in line:
                    if float(line.split(":")[-1].split("\n")[0]) != 0:
                        temps.append(float(line.split(":")[-1].split("\n")[0]))
                if "Instance" in line:
                    instance = line.split()[-1]
                if "Heuristique" in line:
                    heuristique = line.split()[-1]
        compt += 1

    file = open(args.chemin + instance + '-' + str(hash) + '-Summary.txt', 'w')
    file.write("Instance: ")
    file.write(instance)
    file.write("\n")
    file.write("Heuristique: ")
    file.write(heuristique)
    file.write("\n")
    file.write("Makespan moyen (")
    file.write("sur ")
    file.write(str(compt))
    file.write(" instances): ")
    file.write(str(sum(makespan) / len(makespan)))
    file.write("\n")
    file.write("Makespan mini: ")
    file.write(str(min(makespan)))
    file.write("\n")
    file.write("Temps moyen: ")
    file.write(str((sum(temps) / len(temps))))
    file.close

    return temps


if __name__ == '__main__':
    main(sys.argv)
