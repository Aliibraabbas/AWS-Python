import threading
from requests import Session, HTTPError
import time

class TEST():
    def __init__(self):
        self.session = Session()
        self.base_url = "https://5ze43vn695.execute-api.eu-west-1.amazonaws.com/dev"
        self.api_key = "353a0fba-06a4-4b8d-aaa8-175a1f413edb"

    def get_user(self):
        try:
            headers = {
                "x-api-key": self.api_key 
            }
            res = self.session.get(url=f"{self.base_url}/manageUser", headers=headers)
            res.raise_for_status()
            print(f"Informations de l'utilisateur : {res.text}")
        except HTTPError as e:
            print(f"HTTPError: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Erreur : {str(e)}")

    def create_user(self, email):
        try:
            body = {"email": email}
            res = self.session.post(url=f"{self.base_url}/getToken", json=body)
            res.raise_for_status()
            print(f"Réponse de création d'utilisateur : {res.text}")

            # Récupère la clé API (hash_value) de la réponse
            token_api = res.json().get('hash_value')
            if token_api:
                print(f"Token API récupéré : {token_api}")
            else:
                print("Erreur : Aucun token trouvé dans la réponse.")
        except HTTPError as e:
            print(f"HTTPError: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Erreur : {str(e)}")

    def run_threads(self):
        # Récupère les informations de l'utilisateur avec la clé API 
        self.get_user()

        # Ajoute un délai pour s'assurer que l'opération de récupération est terminée
        time.sleep(2)

        # Crée des utilisateurs en parallèle
        emails = ["testuser1@gmail.com", "testuser2@gmail.com"]
        threads = []
        for email in emails:
            thread = threading.Thread(target=self.create_user, args=(email,))
            threads.append(thread)
            thread.start()

        # Attend que tous les threads de création soient terminés
        for thread in threads:
            thread.join()

# Exemple d'utilisation
test = TEST()
test.run_threads()
