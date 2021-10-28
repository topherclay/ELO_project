import os

# so confused by why this has to be this way this way here
import cv2.cv2 as cv2


class Contender:
    DEFAULT_RANK = 1400

    # the maximum adjustment you can get from one game. Also called K-Factor.
    ADJUSTMENT_FACTOR = 16


    def __init__(self, name=None, rank=1400):
        self.name = name
        self.rank = self.check_if_rank_is_valid(rank)
        self.actual_scores = []
        self.expected_scores = []

    @staticmethod
    def check_if_rank_is_valid(rank):
        if rank <= 0:
            rank = 1400
        return rank


    def generate_expected_scores_with_other(self, other):
        # other needs to be also a Contender like self.
        my_expected, others_expected = self.calc_expected_scores_wikipedia_style(self.rank, other.rank)
        self.expected_scores.append(my_expected)
        other.expected_scores.append(others_expected)

    @staticmethod
    def calc_expected_scores_wikipedia_style(rating_of_a, rating_of_b):
        # todo: revisit this to streamline it to have less exponents
        q_of_a = 10 ** (rating_of_a / 400.0)
        q_of_b = 10 ** (rating_of_b / 400.0)
        expected_score_of_a = q_of_a / (q_of_a + q_of_b)
        expected_score_of_b = 1 - expected_score_of_a
        return expected_score_of_a, expected_score_of_b


    def adjust_my_own_rank(self):
        # these better have the same len()
        if not len(self.expected_scores) == len(self.actual_scores):
            raise AttributeError(f"This class didnt have the same amount of expected scores "
                                 f"{len(self.expected_scores)} "
                                 f"and actual scores "
                                 f"{len(self.actual_scores)}")
        sum_of_expected_scores = sum(self.expected_scores)
        sum_of_actual_scores = sum(self.actual_scores)
        new_rank = self.rank + self.ADJUSTMENT_FACTOR * (sum_of_actual_scores - sum_of_expected_scores)
        # clear out scores now that they have been used
        self.actual_scores = []
        self.expected_scores = []
        self.rank = int(new_rank)


class Pokemon(Contender):
    DIRECTORY_OF_CONTENDERS = "cuter_pokemon"


    def __init__(self, name, rank, pathway):
        super().__init__(name, rank)
        # pathway should be direct path from os.path
        self.pathway = pathway

    def get_rank_from_pathway(self):
        rank = os.path.basename(self.pathway)[:4]
        return rank

    def load_image_from_file(self):
        return cv2.imread(self.pathway)


    def rename_file(self):
        new_base = f"{self.rank:04}" + os.path.basename(self.pathway)[4:]
        new_pathway = os.path.join(os.path.dirname(self.pathway), new_base)
        os.rename(self.pathway, new_pathway)





class HeadToHead:
    def __init__(self, pairing=(), winner=None):
        # To declare a winner, set winner to string "lef", "right", or "tie"
        self.contender_a: Contender = pairing[0]
        self.contender_b: Contender = pairing[1]
        self.set_the_contenders_expected_scores()
        if winner:
            self.declare_an_outcome_and_append_actual_scores(winner)

    def set_the_contenders_expected_scores(self):
        self.contender_a.generate_expected_scores_with_other(self.contender_b)


    def declare_an_outcome_and_append_actual_scores(self, outcome):
        results = {"left": [1, 0], "tie": [0.5, 0.5], "right": [0, 1]}

        actual_scores = results[outcome]

        self.contender_a.actual_scores.append(actual_scores[0])
        self.contender_b.actual_scores.append(actual_scores[1])

    def adjust_ranks_for_contenders(self):
        self.contender_a.adjust_my_own_rank()
        self.contender_b.adjust_my_own_rank()






if __name__ == "__main__":
    pass

