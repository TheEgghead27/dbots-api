from simplejson import load

try:
    data = open('data.json', 'r')
except FileNotFoundError:
    data = open('src/data.json', 'r')
data = load(data)
kirilist = tuple(data["kirilist"])
eggs = tuple(data["eggs"])
eggTrigger = data["eggTrigger"]
eggTrigger.append('🥚')  # workaround for user messages with ":egg:" not triggering it
eggTrigger = tuple(eggTrigger)
mmyes = tuple(data['mmyes'])
simp = tuple(data['simp'])
insults = tuple(data['insults'])
spic = tuple(data['spic'])
del data

try:
    fuck = open('recipes.txt', 'r', encoding='utf-8')
except FileNotFoundError:
    fuck = open('src/recipes.txt', 'r', encoding='utf-8')
cookbook = fuck.read()
fuck.close()
del fuck
