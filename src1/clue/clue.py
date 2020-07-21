import termcolor

from logic import Symbol, Not, And, Or, Implication, model_check

# Enter characters, weapons and rooms
characters = ["Mostarda", "Black", "Violeta",
              "Marinho", "Rosa", "Branca"]

weapons = ["faca", "castical", "revolver",
           "corda", "cano", "chave"]

rooms = ["hall", "estar", "cozinha",
         "jantar", "festas", "musica",
         "jogos", "biblioteca", "escritorio"]

cards = characters + weapons + rooms

# Initialize symbols list and knowledge base
symbols = []

knowledge = And()

# Enter number of players
n_players = 4

# Add another player, the cards of player 0 will be the answer
n_players += 1

# Add cards to symbols list
for card in cards:
    for index in range(n_players):
        symbols.append(Symbol(f"{card}{index}"))

# The answer must contain one person, room, and weapon
knowledge = And(
    Or(Symbol("Mostarda0"), Symbol("Black0"), Symbol("Violeta0"),
       Symbol("Marinho0"), Symbol("Rosa0"), Symbol("Branca0")),
    Or(Symbol("faca0"), Symbol("castical0"), Symbol("revoler0"),
       Symbol("corda0"), Symbol("cano0"), Symbol("chave0")),
    Or(Symbol("hall0"), Symbol("estar0"), Symbol("cozinha0"),
       Symbol("jantar0"), Symbol("festas0"), Symbol("musica0"),
       Symbol("jogos0"), Symbol("biblioteca0"), Symbol("escritorio0"))
)

# If one person, room or weapon is in the answer,
# it implicates that the others aren't
for character1 in characters:
    for character2 in characters:
        if character1 != character2:
            knowledge.add(Implication(Symbol(f"{character1}0"),
                          Not(Symbol(f"{character2}0"))))

for weapon1 in weapons:
    for weapon2 in weapons:
        if weapon1 != weapon2:
            knowledge.add(Implication(Symbol(f"{weapon1}0"),
                          Not(Symbol(f"{weapon2}0"))))

for room1 in rooms:
    for room2 in rooms:
        if room1 != room2:
            knowledge.add(Implication(Symbol(f"{room1}0"),
                          Not(Symbol(f"{room2}0"))))

# If one person has a card,
# this card is not the answer and
# no one else has it
for card in cards:
    for index1 in range(n_players):
        for index2 in range(n_players):
            if index1 != index2:
                knowledge.add(Implication(Symbol(f"{card}{index1}"),
                                          Not(Symbol(f"{card}{index2}"))))


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
knowledge.add(Symbol("Black1"))
knowledge.add(Symbol("Rosa1"))
knowledge.add(Symbol("Cano1"))
knowledge.add(Symbol("Hall1"))


check_knowledge(knowledge)
