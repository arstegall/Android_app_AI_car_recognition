Sever je pisan u Python Flask Frameworku

Za pokretanje servera koristi se komanda:
flask run --port [port]

Za pokretanje u produkcijskom okruzenju (server dostupan izvan lokalne mreze):
flask run --host 0.0.0.0 --port 8080

Ukoliko se naide bolji model potrebno je samo zamjeniti cnn_model.h5 sa azuriranim modelom (ime mora ostati isto)