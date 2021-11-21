from flask import Flask
from algo import main as main_algo

app = Flask(__name__)

@app.route('/')
def index():
    babette = ["Tærsklen","Genskær","Sød", "Bordbøn", "Brylluppet", "Drikkevarerne",
        "Højtideligt", "Næsen", "Forbløffet", "Sanser", "Skefuld", "Skildpaddesuppe",
        "Panik", "Tungerne", "Styrke", "Tårerne", "Lyttende", "Vemodig", "Harmonien",
        "Fuldkommen", "Gaffel", "Panden", "Blinis", "Bordfæller", "Overraskelse", "Behag", "Forunderlige", "Mirakler", "Huskede", "Fisker",
        "Overfarten", "Håbet", "Fornyede", "Bølgerne", "Frost", "Bred", "Skummede","Limonade",
        "Sindsstemning", "Jorden", "Sidemand", "Ordrer", "Fornuft", "Gal", "Tung",
        "Modsatte", "Lettere", "Hjertet", "Spiste", "Drak", "Mennesket", "Afvist", "Æde"]
    

    return main_algo(babette)
