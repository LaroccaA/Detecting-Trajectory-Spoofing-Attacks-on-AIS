import pandas as pd
import os
import glob
from pathlib import Path
import time

def converti_e_pulisci_cartella(folder_path):
    """
    Trova tutti i file CSV nella cartella specificata, li converte in Parquet
    con lo stesso nome e cancella il file CSV originale.
    """
    # Converti il percorso in un oggetto Path per una gestione più semplice
    cartella = Path(folder_path)
    
    if not cartella.is_dir():
        print(f"❌ ERRORE: La cartella '{folder_path}' non esiste o non è valida.")
        return

    # Trova tutti i file CSV nella cartella
    file_csv_trovati = list(cartella.glob('*.csv'))
    
    if not file_csv_trovati:
        print(f"⚠️ Nessun file CSV trovato nella cartella '{folder_path}'.")
        return

    print(f"🚀 Trovati {len(file_csv_trovati)} file CSV da convertire in '{folder_path}'...")
    print("-" * 50)

    for csv_path in file_csv_trovati:
        # Determina il nome del file Parquet (stesso nome, estensione .parquet)
        parquet_path = csv_path.with_suffix('.parquet')
        
        # Inizia il tracciamento del tempo
        start_time = time.time()
        
        print(f"🔄 Avvio conversione di: {csv_path.name}")
        
        try:
            # 1. Lettura del file CSV
            # low_memory=False è consigliato per file grandi per una corretta inferenza dei tipi
            df = pd.read_csv(csv_path, low_memory=False)
            
            # 2. Scrittura del file Parquet (usando Snappy per buon bilanciamento velocità/dimensione)
            # index=False evita di scrivere la colonna indice di Pandas nel file Parquet
            df.to_parquet(parquet_path, compression='snappy', index=False)
            
            end_time = time.time()
            
            # 3. Pulizia e verifica dei file
            csv_size_mb = csv_path.stat().st_size / (1024 * 1024)
            parquet_size_mb = parquet_path.stat().st_size / (1024 * 1024)
            
            # 4. Cancellazione del CSV originale
            os.remove(csv_path)
            
            print(f"✅ Conversione e pulizia completate per {csv_path.name}:")
            print(f"   ⏱️ Tempo: {end_time - start_time:.2f}s")
            print(f"   💾 Dimensione CSV: {csv_size_mb:.2f} MB -> Parquet: {parquet_size_mb:.2f} MB")
            print(f"   🗑️ File CSV originale eliminato.")
        
        except Exception as e:
            print(f"❌ ERRORE durante l'elaborazione di {csv_path.name}: {e}")
            if os.path.exists(parquet_path):
                # Se l'errore è avvenuto dopo la scrittura, il CSV è stato cancellato.
                # Se l'errore è avvenuto durante la scrittura, il file Parquet potrebbe
                # essere incompleto. Meglio non cancellare il CSV in caso di errore.
                print(f"   ⚠️ Conversione fallita. Mantenuto il file CSV originale.")
            
        print("-" * 50)

# =========================================================
# === IMPOSTAZIONE DELLA CARTELLA ===
# =========================================================

# TODO: INSERISCI QUI IL PERCORSO COMPLETO DELLA TUA CARTELLA
# Esempio su Windows: r'C:\Users\TuoNome\Documenti\Dati'
# Esempio su Linux/Mac: '/home/tuonome/dati_big'

CARTELLA_DA_ELABORARE = '/home/al3th3ia/Scrivania/Cybersecurity/Dataset/AIS_Daily_Data/' # <--- SOSTITUISCI QUESTO PERCORSO

# Se vuoi testare lo script nella cartella corrente, puoi lasciarlo così:
#CARTELLA_DA_ELABORARE = os.getcwd() 

# Esegui la funzione
converti_e_pulisci_cartella(CARTELLA_DA_ELABORARE)