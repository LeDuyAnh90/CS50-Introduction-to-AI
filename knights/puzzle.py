from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnave, AKnight)) # A cannot be both knight and knave
    ,Or(And(AKnight,And(AKnave, AKnight)) # If A is knight, then the sentence is true
        ,And(AKnave,Not(And(AKnave, AKnight))) # If A is knave, then the setence is false
    ) 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(And(AKnave, AKnight)) # A cannot be both knight and knave
    , Not(And(BKnave, BKnight)) # B cannot be both knight and knave
    , Or(
        And(AKnight, And(AKnave,BKnave)) # If A is knight then the sentence is true 
        , And(AKnave, Not(And(AKnave,BKnave))) # if A is knave then the setence is false
    )
    , And(BKnight,Not(And(AKnave,BKnave))) # If B is knight then the setence is false
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(And(AKnave, AKnight)) # A cannot be both knight and knave
    , Not(And(BKnave, BKnight)) # B cannot be both knight and knave
    , Or(
        And(AKnight, Or(And(AKnight,BKnight),And(AKnave,BKnave))) # If A is knight then A's setence is true
         ,And(AKnave,Or(And(AKnight,BKnave),And(AKnave,BKnight))) # If A is knave then A's sentence is false
    )
    , Or(
        And(BKnight,Or(And(BKnight,AKnave),And(BKnave,AKnight))) # If B is knight then B's setence is true
        , And(BKnave,Or(And(AKnight,BKnight),And(AKnave,BKnave))) # If B is knave then B's setence is false
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
   Not(And(AKnave, AKnight)) 
    , Not(And(BKnave, BKnight)) 
    , Not(And(CKnave, CKnight))
    , Or(
        And(BKnight, Or(And(AKnight,AKnave),And(AKnave,Not(AKnave))),CKnave) # If B is knight
        , And(BKnave,Or(And(AKnight,AKnight),And(AKnave,Not(AKnight))),Not(CKnave)) # If B is knave
    )
    , Or(
        And(CKnight,AKnight) # If C is knight
        , And(CKnave,Not(AKnight)) # If C is knave
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
