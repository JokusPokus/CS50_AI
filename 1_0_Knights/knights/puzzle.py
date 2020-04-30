from logic import *


def general_rules(person):
    """Each person is a Knight or a Knave, but not both (exclusive OR).
    The person parameter is a string A, B, or C.
    """
    is_knight = person + "Knight"
    is_knave = person + "Knave"
    return Biconditional(eval(is_knight), Not(eval(is_knave)))


def sentence_true_or_false(person, sentence):
    """A sentence is true iff its author is a Knight.
    A sentence is false iff its author is a Knave.
    """
    is_knight = person + "Knight"
    return Biconditional(eval(is_knight), sentence)


# Simple propositions that will be tested below
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# *********************************************
# Puzzle 0
# A says "I am both a knight and a knave."
sentenceA = And(AKnight, AKnave)

knowledge0 = And(
    general_rules("A"),
    sentence_true_or_false("A", sentenceA)
)

# *********************************************
# Puzzle 1
# A says "We are both knaves."
sentenceA = And(AKnave, BKnave)
# B says nothing.

knowledge1 = And(
    general_rules("A"),
    general_rules("B"),
    sentence_true_or_false("A", sentenceA)

)

# *********************************************
# Puzzle 2
# A says "We are the same kind."
sentenceA = And(
    Biconditional(AKnight, BKnight),
)
# B says "We are of different kinds."
sentenceB = And(
    Biconditional(AKnight, BKnave),
)

knowledge2 = And(
    general_rules("A"),
    general_rules("B"),
    sentence_true_or_false("A", sentenceA),
    sentence_true_or_false("B", sentenceB)
)

# *********************************************
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentenceA_1 = AKnight
sentenceA_2 = AKnave
# B says "A said 'I am a knave'."
# B says "C is a knave."
sentenceB_1 = sentence_true_or_false("A", sentenceA_2)
sentenceB_2 = CKnave
# C says "A is a knight."
sentenceC = AKnight

knowledge3 = And(
    general_rules("A"),
    general_rules("B"),
    general_rules("C"),
    Or(
        sentence_true_or_false("A", sentenceA_1),
        sentence_true_or_false("A", sentenceA_2)
    ),
    sentence_true_or_false("B", sentenceB_1),
    sentence_true_or_false("B", sentenceB_2),
    sentence_true_or_false("C", sentenceC)
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
