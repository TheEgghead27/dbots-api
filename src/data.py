from simplejson import load

with open('data.json', 'r') as data:
    data = load(data)
    kirilist = tuple(data["kirilist"])
    eggs = tuple(data["eggs"])
    eggTrigger = data["eggTrigger"]
    eggTrigger.append('🥚')  # workaround for user messages with ":egg:" not triggering it
    eggTrigger = tuple(eggTrigger)
    mmyes = tuple(data['mmyes'])
    simp = tuple(data['simp'])
    insults = tuple(data['insults'])
del data

fuck = open('recipes.txt', 'r', encoding='utf-8')
cookbook = fuck.read()
fuck.close()
del fuck
