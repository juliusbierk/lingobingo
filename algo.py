import numpy as np
from collections import Counter



def create_card(n_card_words, n_words, earliest_win):
    idxs = np.arange(n_words)
    subtract = 1 + max(0, np.random.poisson(n_card_words * (n_words - earliest_win) / n_words) - 1)
    subtract = min(subtract, n_card_words - 2)
    first = np.random.choice(idxs[:earliest_win], size=n_card_words - subtract, replace=False)
    last = np.random.choice(idxs[earliest_win:], size=subtract, replace=False)
    return np.random.permutation(np.append(first, last))


def create_cards(words, n_cards=20, rows=3, columns=5, empty=2, win_distance_to_end=10):
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
    e = np.ones((len(cards), rows, empty), dtype=np.int64) * len(words)
    cards = np.concatenate((cards, e), axis=2)
    cards = np.apply_along_axis(np.random.permutation, 2, cards)

    return words, np.asarray(words + ['         '])[cards], empty


def play(words, all_cards, empty):
    cards, rows, columns = all_cards.shape
    winner_info = []

    for game in range(1, rows + 1):
        score = [[0 for _ in range(rows)] for _ in range(cards)]
        restart = False
        old_winners = []
        winners = []

        for w in words:
            for i in range(cards):
                for j, r in enumerate(all_cards[i]):
                    if w in r:
                        score[i][j] += 1

            n_winners = 0
            for i in range(cards):
                if i in old_winners:
                    continue

                if sum(np.array(score[i]) == (columns - empty)) == game:
                    n_winners += 1
                    winners.append(i)

            if n_winners > 0:
                st = f'Row game {game} has {n_winners} winner(s) {winners} at word "{w}"'
                winner_info.append(st)
                print(st)
                old_winners.extend(winners)
                winners = []
        print()
        winner_info.append(None)
    return winner_info

def make_html(all_cards, winner_info, color='#eee123', fontsize='h3', cards_per_page=3):
        # make website
    html = '''<html>
    <head>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" type="text/css"  href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    <style>


    body {
      -webkit-print-color-adjust: exact !important;
      color-adjust: exact;
    }

    @media print {
      .visible-print  { display: inherit !important; }
      .hidden-print   { display: none !important; }
      -webkit-print-color-adjust: exact; 
    }

    @media print {
        tr.vendorListHeading {
            background-color: #1a4567 !important;
            -webkit-print-color-adjust: exact; 
        }
    }

    @media print {
        .vendorListHeading th {
            color: white !important;
        }
    }
    table {
      border: 1px solid black;
      table-layout: fixed;
      width: 200px;
    }

    th,
    td {
      border: 1px solid black;
      width: 100px;
      height: 100px;
      overflow: hidden;
    }
    @media print {
        .pagebreak { page-break-before: always; } /* page-break-after works, as well */
    }
    h1 { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 700;  } h3 { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 700;  } p { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 400; blockquote { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 400; pre { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 400;  }
    </style>
    </head>
    <body>\n
    '''
    for i, c in enumerate(all_cards):
        if i > 0 and i % cards_per_page == 0:
            html += '<div class="pagebreak"> </div>\n'
        html += f'<br><h3>Card {i}</h3><br>\n'
        html += '<table class="table table-bordered">\n'
        for r in c:
            html += '<tr>\n'
            for v in r:
                if len(v.replace(' ', '')) > 0:
                    html += f'<th style="background-color: {color} !important" class="text-center"><{fontsize}>{v}</{fontsize}></th>\n'
                else:
                    html += f'<th>{v}</th>\n'
            html += '</tr>\n'
        html += '</table>\n<br><br>\n'

    html += '<div class="pagebreak"> </div>\n'
    for st in winner_info:
        if st is None:
            html += f'\n<br>'
        else:
            html += f'\n<br>{st}<br>'
    html += '<br><br></body></html>'
    return html

def main(words, n_cards=20, rows=3, columns=5, empty=2, color='#eee123'):
    words, cards, empty = create_cards(words, n_cards=n_cards, rows=rpws, columns=columns, empty=empty)  
    winner_info = play(words, cards, empty)
    html = make_html(cards, winner_info, color)
    return html


if __name__ == '__main__':
    babette = ["Tærsklen","Genskær","Sød", "Bordbøn", "Brylluppet", "Drikkevarerne",
        "Højtideligt", "Næsen", "Forbløffet", "Sanser", "Skefuld", "Skildpaddesuppe",
        "Panik", "Tungerne", "Styrke", "Tårerne", "Lyttende", "Vemodig", "Harmonien",
        "Fuldkommen", "Gaffel", "Panden", "Blinis", "Bordfæller", "Overraskelse", "Behag", "Forunderlige", "Mirakler", "Huskede", "Fisker",
        "Overfarten", "Håbet", "Fornyede", "Bølgerne", "Frost", "Bred", "Skummede","Limonade",
        "Sindsstemning", "Jorden", "Sidemand", "Ordrer", "Fornuft", "Gal", "Tung",
        "Modsatte", "Lettere", "Hjertet", "Spiste", "Drak", "Mennesket", "Afvist", "Æde"]
    main(babette)
    