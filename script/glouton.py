import random


def recherche_tache(inst, t, prio="SPT", rnd=0):
    # Recherche la tâche prioritaire à un instant t, selon l'heuristique.
    # Input :
    # --- inst: Objet Instance
    # --- t: int temps
    # --- prio: string "SPT" or "LPT"
    # --- random: double, % d'avoir une heuristique randomisé
    # Output: None

    tache_possible = []
    # Pour chaque jobs
    for j in inst.jobs_list:
        if j.state != "Done":
            # Si la machine de la tâche en cours du job et libre
            if j.current_task.machine.state == "Free":
                # On ajoute cette tache à la liste de tache possible
                tache_possible.append(j.current_task)

    if len(tache_possible) != 0:
        if random.random() < rnd:
            maxi_task = random.sample(tache_possible, 1)[0]
            mini_task = random.sample(tache_possible, 1)[0]
        # Recherche du max parmis les taches possibles
        else:
            for k in range(len(tache_possible)):
                if prio == "LPT":
                    maxi = -1
                    for e in tache_possible:
                        if e.duration > maxi:
                            if e.machine.state == "Free":
                                maxi = e.duration
                                maxi_task = e
                elif prio == "SPT":
                    mini = 1000000
                    for e in tache_possible:
                        if e.duration < mini:
                            if e.machine.state == "Free":
                                mini = e.duration
                                mini_task = e
    try:
        if prio == "LPT":
            maxi_task.job.update_current_task(maxi_task.taskID, t)
            try:
                tache_possible.remove(maxi_task)
            except:
                pass
        elif prio == "SPT":
            mini_task.job.update_current_task(mini_task.taskID, t)
            try:
                tache_possible.remove(mini_task)
            except:
                pass
    except UnboundLocalError:
        pass


def finish(instance):
    for resource in instance.jobs_list:
        if resource.state == "Not Done":
            return False
    return True


def makespan(instance):
    maxi = -1
    for j in instance.jobs_list:
        for t in j.task_list:
            if t.finishDate > maxi:
                maxi = t.finishDate
    return maxi


def heuristique_gloutone(instance, prio="SPT", rnd=0, verbose=0):
    # Heuristique gloutonne
    # Input:
    # --- inst: Objet Instance
    # --- rnd: double, probabilité d'avoir un choix aléatoire dans l'heuristique
    # --- Verbose: int, niveau de verbose
    # Output: None
    time = 0
    recherche_tache(instance, time, prio, rnd)
    time += 1
    while time < 10000:
        if finish(instance):
            break
        if verbose > 0:
            print("Temps", time)
        for res in instance.resource_list:
            if verbose > 0:
                print(res)
            if res.current_task == -1:
                recherche_tache(instance, time, prio, rnd)
            elif res.current_task.finishDate <= time:
                res.current_task.deallocate_to_ressource("Done")
                recherche_tache(instance, time, prio, rnd)
        time += 1
    return makespan(instance)
