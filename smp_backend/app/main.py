
from fastapi import FastAPI, WebSocket
from app.routes import example  # Importa il file delle rotte

import requests

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origini consentite (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi (GET, POST, ecc.)
    allow_headers=["*"],  # Permetti tutti gli header
)

@app.get("/")
def read_root():
    cik = "0000320193"  # Apple Inc.
    base_url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    headers = {"User-Agent": "smp__back/1.0 (octavianfusari@gmail.com)"}
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Accedi ai filing recenti
        filings = data.get("filings", {}).get("recent", {})
        
        # Filtra i documenti di tipo 10-K
        reports = []
        for idx, form in enumerate(filings.get("form", [])):

            if form == "10-K":  # Filtra solo i documenti 10-K
                print(form == "10-K")
                accession_number = filings["accessionNumber"][idx]
                document = filings["primaryDocument"][idx]
                
                # Costruisci l'URL per il documento
                report_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{accession_number.replace('-', '')}/{document}"
                reports.append(report_url)
                for report in reports:
                    print(report)
                return{"message": reports}
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")


    
    """ cik="0000320193"

    base_url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    headers = {"User-Agent": "smp__back/1.0 (octavianfusari@gmail.com)"}
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        
        return{"message": response.json()}
    else:
        raise Exception("fallimento nel fatching dei dati") """


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")


# Includi le rotte
app.include_router(example.router)