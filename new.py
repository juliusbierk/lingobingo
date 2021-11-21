import numpy as np
from collections import Counter



def create_card(n_card_words, n_words, earliest_win):
    idxs = np.arange(n_words)
    subtract = 1 + max(0, np.random.poisson(n_card_words * (n_words - earliest_win) / n_words) - 1)
    subtract = min(subtract, n_card_words - 2)
    first = np.random.choice(idxs[:earliest_win], size=n_card_words - subtract, replace=False)
    last = np.random.choice(idxs[earliest_win:], size=subtract, replace=False)
    return np.random.permutation(np.append(first, last))


def create_cards(words, n_cards=20, rows=3, columns=5, win_distance_to_end=10):
    words = [x.upper() for x in words]
    rows = 3
    columns = 5
    earliest_win = len(words) - win_distance_to_end

    cards = np.array([create_card(rows * columns, len(words), earliest_win).reshape((rows, columns))
        for _ in range(2 * n_cards)])

    scores = np.zeros((len(cards), rows), dtype=np.int64)
    winner_line = 10000 + np.zeros(len(cards), dtype=np.int64)
    winner_all = 10000 + np.zeros(len(cards), dtype=np.int64)

    for t in range(len(words)):
        card_number, row_number, column_number = np.where(cards == t)
        scores[card_number, row_number] += 1

        line_winner_card_numbers, _ = np.where(scores == columns)
        winner_line[line_winner_card_numbers] = np.minimum(t, winner_line[line_winner_card_numbers])

        all_winner_card_numbers = np.where(np.sum(scores, axis=1) == rows * columns)
        winner_all[all_winner_card_numbers] = np.minimum(t, winner_all[all_winner_card_numbers])

    dead = np.zeros(len(cards), dtype=np.bool_)
    for ri in range(n_cards, len(cards)):
        # remove card
        remove_winner_input = winner_line if ri % 2 == 0 else winner_all
        remove_winner_input = remove_winner_input + 1000000 * dead 
        idxs, c = np.unique(remove_winner_input, return_counts=True)
        idxs[c == 1] += 10000
        remove_i = np.where(remove_winner_input == np.min(idxs))[0][0]
        dead[remove_i] = 1

    cards = cards[~dead, :, :]
    return np.asarray(words)[cards]


if __name__ == '__main__':
    babette = ["Tærsklen","Genskær","Sød", "Bordbøn", "Brylluppet", "Drikkevarerne",
        "Højtideligt", "Næsen", "Forbløffet", "Sanser", "Skefuld", "Skildpaddesuppe",
        "Panik", "Tungerne", "Styrke", "Tårerne", "Lyttende", "Vemodig", "Harmonien",
        "Fuldkommen", "Gaffel", "Panden", "Blinis", "Bordfæller", "Overraskelse", "Behag", "Forunderlige", "Mirakler", "Huskede", "Fisker",
        "Overfarten", "Håbet", "Fornyede", "Bølgerne", "Frost", "Bred", "Skummede","Limonade",
        "Sindsstemning", "Jorden", "Sidemand", "Ordrer", "Fornuft", "Gal", "Tung",
        "Modsatte", "Lettere", "Hjertet", "Spiste", "Drak", "Mennesket", "Afvist", "Æde"]

    cards = create_cards(babette)  
    print(cards)