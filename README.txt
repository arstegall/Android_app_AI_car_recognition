***
Slike za treniranje i test nisu ukljucene u ovu mapu zbog velicine
Moguce ih skinuti sa:
http://ai.stanford.edu/~jkrause/cars/car_dataset.html
***

AndroidApp:
	- android aplikacija
	- odabire se slika i salje na server za obradu
	- mogucnost odabira slike iz galerije ili direktno slikanje nove slike
	- server vraca marku auta, model auta i koliko je model siguran te se to prikazuje u aplikaciji

********************************************************************************
CNNTreniranje:
	- kod u kojem je definirana konvolucijska mreza
	- izvrsava se treniranje modela
	- spremanje modela u zasebnu datoteku

********************************************************************************
Server:
	- sluzi za prepoznavanje slike i vracanje podataka o slici
	- prima sliku u base64 formatu, dekodira je i sprema na lokalnu pohranu servera
	- ucitava se vec istrenirani model (h5 format)
	- s obzirom na dani istrenirani model prepozaje sto je na slici
	- vraca marku auta, model auta, koliko je model siguran
	- server je pisan u Python Flask aplikaciji
	- samo prepoznavanje vrti se u zasebnoj skripti
	- koristimo cache da ubrzamo obradu
	- server testiran i trenutno postavljen na AWS ec2 instanci
