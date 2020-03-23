import json


def loader(name='ft06', ensemble=True):
    # Input: String, the name of a instances listed in the json file
    # Output:
    #  -number of machine
    #  -number of jobs
    #  -matrix (machine / duration)
    with open('data/instances.json') as json_data:
        data = json.load(json_data)

        for i, f in enumerate(data):
            if ensemble == True:
                if f['name'] == name:
                    index = i
                    break
            else:
                if f['name'][:2] == name:
                    index = i
                    break
        nb_machine = data[index]['machines']
        nb_jobs = data[index]['jobs']
        optimum = data[index]['optimum']


    file = open("data/instances/" + name, "r")
    tab = []
    for i, line in enumerate(file):
        if name[:2]== 'ta':
            if i > 0:
                tab.append([int(e) for e in line.split()])
        else:
            if i > 4:
                tab.append([int(e) for e in line.split()])

    return {"nb_machine":nb_machine, "nb_jobs":nb_jobs, "problem":tab}, optimum


def separate(matrix):
    # Input: Array, the machine / duration matrix (from loader)
    # Output:
    # Array, machine matrix
    # Array, duration matrix
    machine = []
    duration = []
    for i, job in enumerate(matrix):
        machine.append([])
        duration.append([])
        for k, e in enumerate(job):
            if k % 2 == 0:
                # Machine
                machine[i].append(e)
            else:
                # Durée
                duration[i].append(e)
    return machine, duration
