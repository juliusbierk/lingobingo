import numpy as np
from collections import defaultdict
from itertools import combinations
from tqdm import tqdm
import webbrowser


# input

rows = 3
columns = 6
empty = 1

cards = 35

color = '#AA0522'
fontsize = 'h1'   # choose between 'h1, h2, h3, h4, h5, h6'
cards_per_page = 3

babette = ["Tærsklen","Genskær","Sød", "Bordbøn", "Brylluppet", "Drikkevarerne",
    "Højtideligt", "Næsen", "Forbløffet", "Sanser", "Skefuld", "Skildpaddesuppe",
    "Panik", "Tungerne", "Styrke", "Tårerne", "Lyttende", "Vemodig", "Harmonien",
    "Fuldkommen", "Gaffel", "Panden", "Blinis", "Bordfæller", "Overraskelse", "Behag", "Forunderlige", "Mirakler", "Huskede", "Fisker",
    "Overfarten", "Håbet", "Fornyede", "Bølgerne", "Frost", "Bred", "Skummede","Limonade",
    "Sindsstemning", "Jorden", "Sidemand", "Ordrer", "Fornuft", "Gal", "Tung",
    "Modsatte", "Lettere", "Hjertet", "Spiste", "Drak", "Mennesket", "Afvist", "Æde"]

frank = ["bornholmske", "løgringe", "Møn", "fiskevognen", "æggeblomme", "smag",
    "østersølaks", "sigtebrød", "overdådigt", "silede", "etnisk", "bourgogne", "Flora Danica",
    "ødelægge", "zenagtig", "regime", "bolde", "forhaven", "toget", "nervøs", "Sankt Hans",
    "Skagen", "mestendels", "konverserede", "anekdote", "kollega", "Lolland", "mønsterbrydere",
    "ophav", "rævesovs", "selskabet", "gravad", "røget", "flovhed", "nysgerrigt", "knække",
    "græde", "låret", "antog", "rødmede", "sitrede", "ribben", "badetur", "vinglas", "bålet",
    "nippede", "fuld", "havet", "stop", "guldbelagte", "flækkede", "smørblomst", "skjorte",
    "blodet", "bølgeslag", "pyt", "høfligt", "køkkenbordet", "ked", "Japan"]

trold = ["desserter", "kaminen", "floden", "findeløn", "leben", "tilfreds", "sovsle", "rosengrenene", "nyheden",
    "herligt", "forberede", "morsom", "bisamrotten", "lækreste", "sang",  "livsvisdom", "unødvendighed", "perlediademet",
    "papirlygter", "dagslys", "kartoffelkælderen", "rosiner", "mandler", "syltede lotus", "ingefær", "sukker", "muskatblomme",
    "citron", "rønnebærlikør", "kulør", "smørrebrødsfade", "nødder", "bær", "skorzonnérrødder", "hvedeaks", "pandekagedej",
    "syltetøjskrukker", "hæderspladserne", "fineste", "hilste", "oplyste", "tønde", "skåle", "birkebark", "kræmmerhuse",
    "hurrasle", "hjerte", "hoppen", "svansen", "skovånderne", "mussepar", "forlov", "augustmånen", "abrikos", "mystisk",
    "skygge"]

words = [x.upper() for x in trold]

winner_word_number = len(words) - 7

optimization = 1500


# code
assert len(words) > 2 * (rows * (columns - empty)), "Need more words"
assert len(words) == len(set(words)), "A word is repeated!"
assert len(words) > 5 + winner_word_number, "Winner word should come earlier"

potential_all_cards = []
for _ in tqdm(range(optimization)):
    used_combinations = defaultdict(list)

    def gen_line(w):
        line = tuple(np.random.choice(w, size=columns - empty, replace=False))
        while set(line) in used_combinations[0]:
            line = tuple(np.random.choice(w, size=columns - empty, replace=False))
        return line


    def row_condition(rows, row):
        rows = list(rows) + [row]
        for i in range(len(rows)):
            for tup in combinations(np.arange(len(rows)), i + 1):
                s = set()
                for j in tup:
                    s = set.union(s, rows[j])
                    if s in used_combinations[i]:
                        return True
        return False


    all_cards = []

    for i in range(cards):
        while True:
            gen_rows = []
            used_words = []
            for j in range(rows):
                row = gen_line([w for w in words if w not in used_words])
                while row_condition(gen_rows, row):
                    row = gen_line([w for w in words if w not in used_words])
                gen_rows.append(row)
                for w in row:
                    used_words.append(w)

            valid = False
            for w in used_words:
                if words.index(w) >= winner_word_number:
                    valid = True
                    break
            if valid:
                break

        # Accepted:
        for i in range(len(gen_rows)):
            for tup in combinations(np.arange(len(gen_rows)), i + 1):
                s = set()
                for j in tup:
                    s = set.union(s, gen_rows[j])
                    used_combinations[i].append(s)

        gen_rows = [list(np.random.permutation(list(row) + ["         "] * empty)) for row in gen_rows]

        all_cards.append(gen_rows)

    # play:
    score = [[0 for _ in range(rows)] for _ in range(cards)]
    game = 1
    restart = False
    winners = []
    winner_words = []
    for w in words:
        for i in range(cards):
            for j, r in enumerate(all_cards[i]):
                if w in r:
                    score[i][j] += 1
        n_winners = 0
        for i in range(cards):
            if sum(np.array(score[i]) == (columns - empty)) == game:
                n_winners += 1
                winners.append(i)
                winner_words.append(w)

        if n_winners >= 2:
            restart = True
            break
        if n_winners == 1:
            game += 1

    if restart:
        continue

    if len(set(winners)) != len(winners):
        continue

    potential_all_cards.append(all_cards)

if len(potential_all_cards) == 0:
    print('Error! Cannot make a set that works')
    exit()

scores = [0 for _ in range(len(potential_all_cards))]
for card_i, all_cards in enumerate(potential_all_cards):
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
                if n_winners == 1:
                    scores[card_i] += game / 10**len(old_winners)
                else:
                    scores[card_i] -= 0.1 * n_winners * game / 10**len(old_winners)

                old_winners.extend(winners)
                winners = []

i = np.argmax(scores)
all_cards = potential_all_cards[i]


# play:
score = [[0 for _ in range(rows)] for _ in range(cards)]
game = 1
restart = False
winners = []
winner_words = []
for w in words:
    for i in range(cards):
        for j, r in enumerate(all_cards[i]):
            if w in r:
                score[i][j] += 1
    n_winners = 0
    for i in range(cards):
        if sum(np.array(score[i]) == (columns - empty)) == game:
            n_winners += 1
            winners.append(i)
            winner_words.append(w)

    if n_winners >= 2:
        restart = True
        break
    if n_winners == 1:
        game += 1

print('Winners are card numbers (zero-indexed):', winners)
print('Winner words are', winner_words)
print("\n========== CARDS: ===========\n")

ci = 0
for gen_rows in all_cards:
    print(f'------- Card # {ci} --------')
    ci += 1
    for i in range(rows):
        for j in range(columns):
            print(' | ' + gen_rows[i][j], end='')
        print(' | ')
    print("\n\n")


# play:
print()
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
h1 { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; } h3 { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 700; line-height: 15.4px; } p { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 400; line-height: 20px; } blockquote { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 400; line-height: 30px; } pre { font-family: Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif; font-style: normal; font-variant: normal; font-weight: 400; line-height: 18.5714px; }
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

with open('website.html', 'w') as f:
    f.write(html)

webbrowser.open('website.html')
