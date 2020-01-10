import json


def loader(name='abz5'):
    # Input: String, the name of a instances listed in the json file
    # Output:
    #  -number of machine
    #  -number of jobs
    #  -matrix (machine / duration)
    with open('../data/instances.json') as json_data:
        data = json.load(json_data)

        for i, f in enumerate(data):
            if f['name'] == name:
                index = i
                break
        nb_machine = data[index]['machines']
        nb_jobs = data[index]['jobs']

    file = open("data/instances/" + name, "r")
    tab = []
    for i, line in enumerate(file):
        if i > 4:
            tab.append([int(e) for e in line.split()])

    return nb_machine, nb_jobs, tab


def separate(matrix):
    # Input: Array, the machine / duration matrix (from loader)
    # Output:
    # Array, machine matrix
    # Array, duration matrix
    machine = []
    duration = []
    for i, job in enumerate(matrix[1:]):
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
