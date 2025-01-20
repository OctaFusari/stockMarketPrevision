
from fastapi import FastAPI, WebSocket
from app.routes import example  # Importa il file delle rotte

import requests

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
#from imblearn.over_sampling import SMOTE

#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout
#from tensorflow.keras.optimizers import Adam

from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import re
import time
from pydantic import BaseModel

app = FastAPI()
# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origini consentite (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi (GET, POST, ecc.)
    allow_headers=["*"],  # Permetti tutti gli header
)

# Pydamic value per poter dare un formato aidati provenienti dal frontend
class dataFE_model(BaseModel):
    name: str
    modello: str

@app.post("/")
def read_root(dataFE: dataFE_model):
    #esempio 0001018724 -> amazon

    base_url = f'https://data.sec.gov/submissions/CIK{dataFE.name}.json'
    headers = {"User-Agent": "smp__back/1.0 (octavianfusari@gmail.com)"}
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        filings = data.get("filings", {}).get("recent", {})
        
        # Cerca i documenti 10-K dopo che si è fatta la ricerca con EDGAR
        for idx, form in enumerate(filings.get("form", [])):
            if form == "10-K":
                accession_number = filings["accessionNumber"][idx]
                document = filings["primaryDocument"][idx]
                
                # Costruisci l'URL per il documento
                report_url = f"https://www.sec.gov/Archives/edgar/data/{dataFE.name.lstrip('0')}/{accession_number.replace('-', '')}/{document}"

                # Scarica il contenuto del file
                time.sleep(1)  # Rispetta il limite di 10 richieste al secondo
                report_response = requests.get(report_url, headers=headers)
                
                if report_response.status_code == 200:
                    # Analizza il contenuto HTML
                    report_response.encoding = 'utf-8-sig'
                    soup = BeautifulSoup(report_response.text, "html.parser")

                    text = soup.get_text()  # Rimuove i tag HTML
                    text = re.sub(r'\s+', ' ', text)  # Rimuove spazi multipli
                    text = re.sub(r'[^\w\s]', '', text)  # Rimuove simboli

                    #DATASET PRESO DA KAGGLE -> https://www.kaggle.com/datasets/aaron7sun/stocknews/data
                    df2 = pd.read_csv(open("/home/octavian/stockMarketPrediction/smp_backend/app/Combined_News_DJIA.csv", "r"), encoding='ISO-8859-1')
                    
                    # Unisci le colonne dei titoli in un unico testo
                    print("\nUnione le colonne relative ai titoli...")
                    df2['Combined_News'] = df2.iloc[:, 2:27].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

                    # Rimuovi eventuali righe con valori nulli
                    df2.dropna(inplace=True)
                    
                    # Rinomina colonne per chiarezza
                    df2 = df2.rename(columns={"Label": "Sentiment"})

                    # Pre-processing: Vectorizing e appresentazione numerica
                    vectorizer = TfidfVectorizer(max_features=5000)
                    X = vectorizer.fit_transform(df2["Combined_News"]).toarray()
                    y = np.array(df2["Sentiment"])

                    # Divisione del dataset in training e test set
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    #addestramento di sklearn e un modello di tipo randomforest e svm anzichè la rete neurale, uso entrambi(randomforest e svm) e poi vedo quale dei due ha il risultato migliore
                    svc__OBJ = SVCmodel(text, vectorizer,  X_train, y_train, X_test, y_test)
                    rf__OBJ = RandomForestModel(text, vectorizer,  X_train, y_train, X_test, y_test)

                    if dataFE.modello == "svc__OBJ":
                        return{"message": svc__OBJ}
                    else:
                        return{"message": rf__OBJ}
                    
                else:
                    raise Exception(f"Fallimento nel caricare il report: {report_response.status_code}")
    else:
        raise Exception(f"Failed nel prendere i dati status: {response.status_code}")


def RandomForestModel(text, vectorizer, X_train, y_train, X_test, y_test):
    # Creazione del modello Random Forest ottimizzato
    model = RandomForestClassifier(n_estimators=500, max_depth=20, random_state=42)

    # Addestramento
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Accuratezza e report
    print("\nAccuratezza:", accuracy_score(y_test, y_pred))
    print("\nClassificazione del report:")
    print(classification_report(y_test, y_pred))

    # Previsione
    previsione = ""
    if text:
        new_vector = vectorizer.transform([text.lower()]).toarray()
        prediction = model.predict(new_vector)
        previsione = (
            "\nPrevisione: è probabile che il mercato salga."
            if prediction == 1
            else "\nPrevisione: è probabile che il mercato scenda."
        )

    return {
        "previsione": previsione,
        "classificazione": classification_report(y_test, y_pred),
        "accuratezza": accuracy_score(y_test, y_pred),
    }


def SVCmodel(text, vectorizer, X_train, y_train, X_test, y_test):
    # Creazione del modello SVM con pipeline
    model = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1, gamma=0.1, probability=True))

    # Addestramento
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Accuratezza e report
    print("\nAccuratezza:", accuracy_score(y_test, y_pred))
    print("\nClassificazione del report:")
    print(classification_report(y_test, y_pred))

    # Previsione
    previsione = ""
    if text:
        new_vector = vectorizer.transform([text.lower()]).toarray()
        prediction = model.predict(new_vector)
        previsione = (
            "\nPrevisione: è probabile che il mercato salga."
            if prediction == 1
            else "\nPrevisione: è probabile che il mercato scenda."
        )

    return {
        "previsione": previsione,
        "classificazione": classification_report(y_test, y_pred),
        "accuratezza": accuracy_score(y_test, y_pred),
    }


#funzione per ottenere il cik delle aziende via il nome
def fetchCIK(dataFE):
    searchUrl = f"https://efts.sec.gov/LATEST/company-search.json?keys={dataFE.name}"
    headers = {"User-Agent": "smp__back/1.0 (octavianfusari@gmail.com)"}

    risppsta = requests.get(searchUrl, headers=headers)
    print(risppsta)

    cik = ""

    if (risppsta.length > 0):
        cik = risppsta[0]._source.cik
    else:
        cik = "Company not found."

    return cik

# Includi le rotte
app.include_router(example.router)


# Creazione del modello su tensorflow
""" model = Sequential([
    Dense(64, input_dim=X_train.shape[1], activation='relu'),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Output binario
])

# Compilazione del modello
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Addestramento del modello
model.fit(X_train, y_train, epochs=10, batch_size=8, validation_data=(X_test, y_test))

# Valutazione del modello
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print("\nAccuratezza:", accuracy_score(y_test, y_pred))
print("\nClassificazione del report:")
print(classification_report(y_test, y_pred)) """