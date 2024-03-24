 # README.md

## API de Publication de Recette

Une API construite avec FastAPI et MongoDB pour gérer les opérations CRUD sur les recettes culinaires, un système d'abonnement utilisant l'API  de notchpay pour assurer le paiement.

---

### Prérequis

- Python 3.8 ou supérieur
- MongoDB installé et en cours d'exécution

---

### Installation

1. **Clonez le dépôt**
```bash
git clone https://github.com/TheBeyonder237/FoodAppAPI.git
cd recette-api
```

2. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

---

### Configuration

Assurez-vous que MongoDB est en cours d'exécution et notez l'URI pour la connexion.

Créez un fichier `.env` dans le répertoire principal et ajoutez l'URI de MongoDB:
```
MONGODB_URI=mongodb://localhost:27017/votre_base_de_donnees
```

---

### Exécution

```bash
python main.py
```

L'API devrait être en cours d'exécution sur `http://127.0.0.1:8000`.

---

### Endpoints

- **Ajouter une recette**
  - `POST /recipe/`
  - Payload: 
    ```json
    {
      "titre": "string",
      "description": "string",
      "ingredients": ["string", ...],
      "instructions": "string",
      "image_url": "string (optionnel)"
    }
    ```

- **Obtenir toutes les recettes**
  - `GET /recipe/`

- **Obtenir une recette par ID**
  - `GET /recipe/{recipe_id}`

- **Mettre à jour une recette par ID**
  - `PUT /recipes/{recipe_id}`
  - Payload (pour les champs que vous souhaitez mettre à jour):
    ```json
    {
      "titre": "string (optionnel)",
      "description": "string (optionnel)",
      "ingredients": ["string", ... (optionnel)],
      "instructions": "string (optionnel)",
      "image_url": "string (optionnel)"
    }
    ```

- **Supprimer une recette par ID**
  - `DELETE /recipe/{recipe_id}`
    
- **Il y a bien evidemment d'autres routes**
---

### Contribution

Les contributions sont les bienvenues! Veuillez créer une `issue` pour les bugs ou les demandes de fonctionnalités, et soumettre une `pull request` pour les contributions de code.

---

### Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

Pour des questions ou des préoccupations, veuillez contacter [davidngoue@thebeyonder.tech].

---

