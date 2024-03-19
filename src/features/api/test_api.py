import json
import unittest
from fastapi.testclient import TestClient
from .api import api
import warnings

# Charger les données de users_db.json
file = open("users_db_bis.json", 'r')
users_db = json.load(file)
file.close()

# Création d'un client de test pour notre API
client = TestClient(api)

class TestAPI(unittest.TestCase):
    def test_is_functional(self):
        # Envoi d'une requête GET à la racine de l'API
        response = client.get('/status')
        # Vérification que la réponse est OK (code 200)
        self.assertTrue(response.status_code == 200, "Test is_functional: FAILED")
        print("Test is_functional: PASSED")

    def test_register_user(self):
        new_user_data = {"username": "test_user", "password": "test_password"}
        # Envoi d'une requête POST à l'endpoint /register avec l'en-tête d'identification
        response = client.request(method="POST", url='/register', json=new_user_data, headers={"identification": "admin:4dmin"})
        # Vérification que la réponse est OK (code 200)
        self.assertTrue(response.status_code == 200, "Test register_user: FAILED")
        print("Test register_user: PASSED")

    def test_remove_user(self):
        old_user_data = {"user": "test_user"}
        # Envoi d'une requête DELETE à l'endpoint /remove_user avec l'en-tête d'identification
        response = client.request(method="DELETE", url='/remove_user', json=old_user_data, headers={"identification": "admin:4dmin"})
        # Vérification que la réponse est OK (code 200)
        self.assertTrue(response.status_code == 200, "Test remove_user: FAILED")
        print("Test remove_user: PASSED")

    def test_predict_from_test(self):
        # Récupérer un utilisateur et son mot de passe à partir du fichier users_db.json
        user, psw = "fdo", "c0ps"
        # Envoi d'une requête GET à l'endpoint /predict_from_test avec l'en-tête d'identification
        response = client.get('/predict_from_test', headers={"identification": f"{user}:{psw}"})
        # Vérification que la réponse est OK (code 200)
        self.assertTrue(response.status_code == 200, "Test predict_from_test: FAILED")
        print("Test predict_from_test: PASSED")

    def test_predict_from_call(self):
        # Envoyer une requête POST à l'endpoint /predict_from_call avec des données d'entrée
        input_data = {
            "place": 10,
            "catu": 3,
            "sexe": 1,
            "secu1": 0.0,
            "year_acc": 2021,
            "victim_age": 60,
            "catv": 2,
            "obsm": 1,
            "motor": 1,
            "catr": 3,
            "circ": 2,
            "surf": 1,
            "situ": 1,
            "vma": 50,
            "jour": 7,
            "mois": 12,
            "lum": 5,
            "dep": 77,
            "com": 77317,
            "agg_": 2,
            "inter": 1,
            "atm": 0,
            "col": 6,
            "lat": 48.60,
            "long": 2.89,
            "hour": 17,
            "nb_victim": 2,
            "nb_vehicules": 1
        }
        response = client.post('/predict_from_call', json=input_data, headers={"identification": "admin:4dmin"})
        # Vérification que la réponse est OK (code 200)
        self.assertTrue(response.status_code == 200, "Test predict_from_call: FAILED")
        print("Test predict_from_call: PASSED")

    def test_train_model(self):
        # Envoyer une requête GET à l'endpoint /train
        response = client.get('/train', headers={"identification": "admin:4dmin"})
        # Vérification que la réponse est OK (code 200)
        self.assertTrue(response.status_code == 200, "Test train_model: FAILED")
        print("Test train_model: PASSED")

#    def test_update_data(self):
#        # Envoyer une requête GET à l'endpoint /update_data
#        response = client.get('/update_data', headers={"identification": "admin:4dmin"})
#        # Vérification que la réponse est OK (code 200)
#        self.assertTrue(response.status_code == 200, "Test update_data: FAILED")
#        print("Test update_data: PASSED")

if __name__ == '__main__':
    # Exécution des tests unitaires
    unittest.main()
