import argparse
import hashlib
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


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
                if "Max Fit:" in line:
                    maxfit = line
                if "Mean Fit:" in line:
                    meanfit = line
                    meanfit = np.array(meanfit.strip("Mean Fit: [").strip("]\n'").split(",")).astype(float)
                    maxfit = np.array(maxfit.strip("Max Fit: [").strip("]\n'").split(",")).astype(float)
                    plot_genetique_fitness(meanfit, maxfit, args.chemin + '-' + str(file))
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


def plot_genetique_fitness(meanfit, maxfit, logger=None):
    """
    :param logger: Logger
    :param meanfit: list
    :param maxfit: list
    :return: None
    """

    plt.plot(1 / np.array(meanfit), '-or', label="Makespan moyen")
    plt.plot(1 / np.array(maxfit), '-ob', label="Makespan mini")
    plt.legend()
    plt.xlabel('=======> Générations')
    plt.ylabel('=======> Makespan')
    plt.grid()
    title = logger

    plt.title(title)
    plt.savefig(logger + ".png")
    plt.clf()


if __name__ == '__main__':
    main(sys.argv)
