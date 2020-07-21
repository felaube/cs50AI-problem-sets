import termcolor

from logic import Symbol, Not, And, Or, Implication, model_check

# Enter characters, weapons and rooms
Mostarda = Symbol("Mostarda")
Violeta = Symbol("Violeta")
Black = Symbol("Black")
Marinho = Symbol("Marinho")
Rosa = Symbol("Rosa")
Branca = Symbol("Branca")

characters = [Mostarda, Black, Violeta,
              Marinho, Rosa, Branca]

faca = Symbol("faca")
castical = Symbol("castical")
revolver = Symbol("revolver")
corda = Symbol("corda")
cano = Symbol("cano")
chave = Symbol("chave")

weapons = [faca, castical, revolver,
           corda, cano, chave]

hall = Symbol("hall")
estar = Symbol("estar")
cozinha = Symbol("cozinha")
jantar = Symbol("jantar")
festas = Symbol("festas")
musica = Symbol("musica")
jogos = Symbol("jogos")
biblioteca = Symbol("biblioteca")
escritorio = Symbol("escritorio")

rooms = [hall, estar, cozinha,
         jantar, festas, musica,
         jogos, biblioteca, escritorio]

# Initialize symbols list and knowledge base
symbols = characters + weapons + rooms

# The answer must contain one person, room, and weapon
knowledge = And(
    Or(Mostarda, Black, Violeta, Marinho, Rosa, Branca),
    Or(faca, castical, revolver, corda, cano, chave),
    Or(hall, estar, cozinha, jantar, festas, musica, jogos,
       biblioteca, escritorio)
)

# If one person, room or weapon is in the answer,
# it implicates that the others aren't
"""
for character1 in characters:
    for character2 in characters:
        if character1 != character2:
            knowledge.add(Implication(character1,
                          Not(character2)))

for weapon1 in weapons:
    for weapon2 in weapons:
        if weapon1 != weapon2:
            knowledge.add(Implication(weapon1,
                          Not(weapon2)))

for room1 in rooms:
    for room2 in rooms:
        if room1 != room2:
            knowledge.add(Implication(room1,
                          Not(room2)))

for character1 in characters:
    for character2 in characters:
        if character1 != character2:
            knowledge.add(Not(And(character1, character2)))

for weapon1 in weapons:
    for weapon2 in weapons:
        if weapon1 != weapon2:
            knowledge.add(Not(And(weapon1, weapon2)))

for room1 in rooms:
    for room2 in rooms:
        if room1 != room2:
            knowledge.add(Not(And(room1, room2)))
"""


def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: YES", "green")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

"""
# There must be a person, room, and weapon.
knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench)
)

# Initial cards
knowledge.add(And(
    Not(mustard), Not(kitchen), Not(revolver)
))

# Unknown card
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench)
))
"""

# Known cards
knowledge.add(Not(Black))
knowledge.add(Not(Rosa))
knowledge.add(Not(cano))
knowledge.add(Not(hall))
knowledge.add(Not(cozinha))
knowledge.add(Not(corda))


knowledge.add(And(
    Or(Not(Violeta), Not(biblioteca), Not(chave)),
    Or(Not(Branca), Not(jantar), Not(revolver)),
    Or(Not(Branca), Not(estar), Not(chave)),
    ))

knowledge.add(And(
    Or(Not(chave), Not(escritorio)),
    Or(Not(Marinho), Not(festas)),
    ))

check_knowledge(knowledge)
