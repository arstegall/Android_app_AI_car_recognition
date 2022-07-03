
from opcode import opname
import os
import json
from flask import Flask, request
from itsdangerous import base64_decode
import hashlib

# inicijalizacija flask aplikacije
app = Flask(__name__)

# ruta na koju se salje zahtjev za prepoznavanje slike
@app.route('/image/<b64>',  methods=['GET'])
def image_recognition(b64):
    try:
        # ucitavamo datoteku koja nam sluzi za cache
        # prepoznavanje slika zna biti sporo pa ce ovakav postupak ubrzati odgovor mobilnoj aplikaciji
        with open("cache_db.json", "r") as f:
            cache_data = f.read()
        if not cache_data:
            cache_data = {}
        # prilagodba tipa podataka
        if not isinstance(cache_data, dict):
            cache_data = json.loads(cache_data)
        # po dogovoru u base64 stringu znak "/" mijenjamo sa "SLASH" stringom kako bi izbjegli probleme prilikom HTTP zahtjeva sa mobilne aplikacije  
        image = b64.replace("SLASH", "/")
        # ako se slika ne moze procitati iz zahtjeva vracamo pogresku
        if not image:
            return {"msg": "Invalid request"}, 400
        
        # provjera ako slika postoji u cacheu
        # radimo hash od slike s obzirom da je hash unikatna vrijednost i lako pohranjiva (malo memorije)
        img_hash = hashlib.md5(image.encode()).hexdigest()
        # ako slika potoji u cacheu ucitavamo vrijednost i vracamo korisniku bez obrade
        if cache_data.get(img_hash):
            return cache_data[img_hash]

        # spremamo sliku na disk kako bi je kod za prepoznavanje slike mogao obraditi
        with open("data/for_validation/image.jpg","wb") as f:
            f.write(base64_decode(image.encode()))

        # pokrecemo kod za prepoznavanje slike
        os.system("python3 car_recognition.py")

        # citamo rezultate
        with open("results.json", "r") as f:
            results = f.read()

        # radimo json koji vracamo mobilnoj aplikaciji
        results = json.loads(results)[0]
        payload = {}
        payload["marka"] = results["label"].split(" ")[0]
        payload["model"] = results["label"].split(" ", 1)[1]
        # pretvaramo prob u postotak
        payload["prob"] = float(results["prob"])*100
        payload["prob"] = str(payload["prob"])

        # ako vec imamo dosta u cache memoriji ocistimo je
        if len(cache_data) > 100:
            cache_data={}
        # dodavanje rezultata slike u cache
        cache_data[img_hash] = payload 
        with open("cache_db.json", "w") as f:
            cache_data = f.write(json.dumps(cache_data))

        return payload
    except Exception as e:
        # ukoliko je doslo do pogreske u izvodenju koda vracamo gresku
        print("ERROR: ", e)
        return {"msg": "Internal Server Error"}, 500

if __name__ == '__main__':
    # Prepoznavanje izvrsavamo na serveru
    # koristimo flask kako bi dobili zahtjev od mobilne aplikacije i vratili odgovor
    app.run()