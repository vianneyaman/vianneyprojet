from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class InformationsModel(BaseModel):
    nom: str
    prenom: str
    contact: str
    sexe: str
#CODE POUR SE CONNECTER LA BASE DE DONNEES personnes
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="personnes",
            user="monuser",
            password="kramo"
        )
        return conn
    except Exception as e:
        print("Erreur de connexion à la base de données:", e)
        raise HTTPException(status_code=500, detail="Erreur de connexion à la base de données.")


#CODE POUR SUPPRIMER UN ELEMENT SPECIFIQUE DE LA BD A PARTIR DE L'ID
@app.delete("/informations/personnes/{id}", response_model=dict)
async def supprimer_information_par_id(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nom, prenom, contact, sexe FROM informations WHERE id = %s", (id,))
        row = cur.fetchone()
        if row:
            cur.execute("DELETE FROM informations WHERE id = %s", (id,))
            conn.commit()
            return {"message": "Information supprimée avec succès", "nom": row[0], "prenom": row[1], "contact": row[2], "sexe": row[3]}
        else:
            raise HTTPException(status_code=404, detail="Information non trouvée ou déjà supprimée")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression de l'information: {e}")
    finally:
        cur.close()
        conn.close()


#CODE POUR SUPPRIMER UN ELEMENT SPECIFIQUE DE LA BD A PARTIR DU NOM
@app.delete("/informations/personnes/nom/{nom}", response_model=dict)
async def supprimer_information(nom: str):
   conn = get_db_connection()
   cur = conn.cursor()
   try :
       cur.execute("SELECT nom, prenom, contact, sexe FROM informations WHERE nom= %s", (nom,))
       row = cur.fetchone()
       if row:
           cur.execute("DELETE FROM informations WHERE nom = %s", (nom,))
           conn.commit()
           return {"message": "Information supprimée avec succès", "nom": row[0], "prenom": row[1], "contact": row[2], "sexe": row[3]}
       else:
           raise HTTPException(status_code=404, detail="Information non trouvée ou deja supprmée")
   except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression de l'information: {e}")
   finally:
       cur.close()
       conn.close()

#CODE POUR METTRE A JOUR MON API DE TELLE SORTE QUE LES VALEURS VIDES
@app.put("/informations/personnes/{id}", response_model=dict)
async def mettre_a_jour_information(id: int, informations: InformationsModel):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE informations SET nom = %s, prenom = %s, contact = %s, sexe = %s WHERE id = %s",
            (informations.nom, informations.prenom, informations.contact, informations.sexe, id)
        )
        conn.commit()
        return {"message": "Information mise à jour avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour de l'information: {e}")
    finally:
        cur.close()
        conn.close()
 

#CODE POUR AJOUTER UN ELEMENT QUELQCONQUE A LA BD
@app.post("/informations/personnes/", response_model=dict)
async def ajouter_informations(informations: InformationsModel):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO informations (nom, prenom, contact, sexe) VALUES (%s, %s, %s, %s)",
            (informations.nom, informations.prenom, informations.contact, informations.sexe)
        )
        conn.commit()
        return {"message": "information ajoutée avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout: {e}")
    finally:
        cur.close()
        conn.close()


#CODE POUR RECUPERER UN ELEMENT QUELQCONQUE A LA BD A PARTIR DE L'iD
@app.get("/informations/personnes/{id}", response_model=dict)
async def récupérer_informations(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nom, prenom, contact, sexe FROM informations WHERE id = %s", (id,))
        row = cur.fetchone()
        if row:
            return {"message": "Information récuperée avec succès", "nom": row[0], "prenom": row[1], "contact": row[2], "sexe":row[3]}
        else:
            raise HTTPException(status_code=404, detail="Information non trouvée")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récuperation de l'information: {e}")
    finally:
        cur.close()
        conn.close()


#CODE POUR RECUPERER UN ELEMENT QUELQCONQUE A LA BD A PARTIR DU NOM
@app.get("/informations/personnes/nom/{nom}", response_model=dict)
async def récupérer_informations(nom: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nom, prenom, contact, sexe FROM informations WHERE nom = %s", (nom,))
        row = cur.fetchone()
        if row:
            return {"message": "Information récuperée avec succès", "nom": row[0], "prenom": row[1], "contact": row[2], "sexe":row[3]}
        else:
            raise HTTPException(status_code=404, detail="Information non trouvée")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la récuperation de l'information: {e}")
    finally:
        cur.close()
        conn.close()
