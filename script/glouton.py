from script.data import loader, separate


def sol_glouton(name='abz5', prio="EDD"):
    # Se placer à une date t égale à la plus petite date de début des opérations
    n_machine, n_job, data = loader('abz5')
    machine, duration = separate(data)
    t = 0
    # construite l'ensemble des opérations pouvant être réalisées à la date t
    dispo_machine = [0]*n_machine
    for i in n_machine:
        dispo_machine[i[0]] = 1
    # sélectionner l'opération (i,j) de plus grande priorité
