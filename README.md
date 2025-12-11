# Detecting Trajectory Spoofing Attacks on AIS

Questo progetto implementa e confronta due architetture avanzate di Autoencoder Ricorrenti per l'identificazione di comportamenti anomali (spoofing GPS, manovre impossibili, derive) nei dati di tracciamento marittimo (AIS).

Il lavoro è focalizzato sull'integrazione di reti a tempo discreto (**LSTM**) e reti a tempo continuo (**LNN**) per modellare la dinamica navale e sviluppare un sistema di allarme robusto e fisicamente informato.

***

## Architetture Ricorrenti a Confronto

Il sistema utilizza Autoencoder addestrati alla ricostruzione per apprendere la firma del movimento "normale". L'anomalia è definita come un alto errore di ricostruzione (MAE).


### 1. LSTM Autoencoder (Long Short-Term Memory) - Approccio a Tempo Discreto
Fornisce un'alternativa tradizionale e potente, basata su un'architettura che gestisce le sequenze temporali in passi discreti.

### 2. Liquid Neural Network (LNN) - Approccio a Tempo Continuo
* **Celle CfC (Closed-form Continuous-time):** Modellano la dinamica del veicolo attraverso la risoluzione di equazioni differenziali. Questo conferisce al modello una stabilità superiore al rumore e un'ottima capacità di catturare l'inerzia e la fisica dei movimenti.
* **Wiring Sparso:** Utilizzo dell'architettura **AutoNCP** (Neural Circuit Policies) per una connettività neurale ispirata alla biologia, che ottimizza l'efficienza e la robustezza del modello.


***

## Classificazione degli Attacchi Testati

Per validare la robustezza dei nostri modelli, la nostra metodologia si concentra sulla capacità di rilevare quattro distinte categorie di anomalie che violano la coerenza fisica e/o dinamica di una traiettoria navale.

1. **Attacco Cinematico (GPS/Teleport)**: 

   * **Incoerenza Creata**: Discontinuità istantanea della posizione (Salto GPS).
   
2. **Speed Spoofing:** 

   * **Incoerenza Creata:** Iniezione di dati di velocità estremamente rumorosi o impossibili (es. accelerazione istantanea).
   
3. **Ghost Ship (Rotta Inversa):**

   * **Incoerenza Creata:** La nave trasmette una velocità nominale, ma il vettore di rotta (COG) è falsificato ($180^\circ$ di errore).

4. **Silent Drift:**

   * **Incoerenza Creata:** La posizione devia lentamente e progressivamente (rampa lineare) mentre la velocità è nominale (simulando un trascinamento o un dirottamento stealth).

***
## Stress Test Multi-Vettoriale e Analisi Comparativa

Abbiamo implementato un test massivo e comparativo, la cui funzione è quella di definire i limiti operativi delle reti ricorrenti rispetto a minacce complesse.

1. **Metodo di Valutazione:** Viene condotto uno **stress test multi-vettoriale** iniettando simultaneamente quattro tipi di attacco **(Teleport, Speed Spoofing, Ghost Ship, Silent Drift)** in un ampio set di dati puliti.

2. **Obiettivo Diagnostico:** L'analisi quantitativa (mostrata nel report finale) non mira solo a contare gli attacchi rilevati, ma soprattutto a identificare le vulnerabilità cinematiche specifiche della rete a tempo discreto (LSTM) per giustificare la superiorità e l'innovazione del modello LNN a tempo continuo.
***

## Metodologia di Rilevamento: Statistical MAE Thresholding ($3\sigma$)

Il sistema di rilevamento degli errori è stato impostato sul calcolo e l'analisi del Mean Absolute Error (MAE) di ricostruzione, con la soglia di allarme definita statisticamente tramite la Regola dei $3\sigma$ sui dati normali.Questa scelta metodologica si basa sull'analisi della distribuzione degli errori generati dai modelli (LSTM e LNN) su traffico lecito. Il sistema di allarme si affida interamente a un confine statistico rigoroso:

   * **Definizione Statistica della Soglia:** Regola della Deviazione Standard ($\mathbf{3\sigma}$). La soglia viene calcolata prendendo come riferimento solo i dati normali, stabilendo un limite oltre il quale l'errore è considerato anomalo:$$Threshold = \mu_{normale} + 3\sigma_{normale}$$

   * **Calcolo:** La soglia è definita come la Media ($\mu$) degli errori di ricostruzione sui dati normali, più tre volte la loro Deviazione Standard ($\sigma$).
   
   * **Funzionamento:** Questo approccio robusto garantisce che il limite sia posizionato in modo da coprire statisticamente il 99.7% dei comportamenti leciti, garantendo al contempo un bassissimo tasso di falsi positivi.

   * Sistema di Allarme Binario: La classificazione è semplice e immediata:$$\text{Alert} = (\text{MAE} > \text{Threshold})$$

***

## Struttura del Repository

Il progetto è organizzato per funzionalità, con cartelle dedicate a ciascun modello e a ciascun tipo di test:

| Cartella / File | Contenuto e Scopo |
| :--- | :--- |
| `Progetto/LNN_V2/LNN.ipynb` | **Training Principale:** Addestramento e configurazione avanzata dell'Autoencoder LNN. |
| `Progetto/LNN_V2/Test.ipynb` | **Test Quantitativo & Qualitativo LNN:** Calibrazione delle soglie e validazione generale delle performance. |
| `Progetto/LNN_V2/Test_Fase_Preliminare/Test_Kinematic_Inconcistency.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Teletrasporto** (salto GPS impossibile). |
| `Progetto/LNN_V2/Test_Fase_Preliminare/Test_Silent_Drift.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Silent Drift** (deriva lenta e insidiosa). |
| `Progetto/LNN_V2/Final_Test_Attacks.ipynb` | **Stress Test:** implementa una pipeline di iniezione attiva degli attacchi per valutare la sensibilità della rete LNN a diverse tipologie di manipolazione cinematica. |
| `Progetto/LSMT_V2/LSMT.ipynb` | **Training Principale:** Addestramento e configurazione avanzata dell'Autoencoder LSMT. |
| `Progetto/LSMT_V2/Test.ipynb` | **Test Quantitativo & Qualitativo LSMT:** Calibrazione delle soglie e validazione generale delle performance. |
| `Progetto/LSMT_V2/Test_Fase_Preliminare/Test_Kinematic_Inconcistency.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Teletrasporto** (salto GPS impossibile). |
| `Progetto/LSMT_V2/Test_Fase_Preliminare/Test_Silent_Drift.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Silent Drift** (deriva lenta e insidiosa). |
| `Progetto/LSMT_V2/Final_vTest_Attacks.ipynb` | **Stress Test:** Implementa una pipeline di iniezione attiva degli attacchi per valutare la sensibilità della rete a diverse tipologie di manipolazione cinematica. |
| `Progetto/Pre-Elaborazione Dati/` | Contiene gli script di pulizia dati (es. `Pulizia Data AIS.ipynb`) e lo **`scaler.joblib`** per la normalizzazione. |
| `set_venv.txt` | Consiste nel file di configurazione dell'ambiente virtuale python per poter eseguire il codice. |
| `report_cybersecurity`| Report del progetto |
| `Presentazione Cybersecurity`| Presentazione del progetto |


***

## Performance di Rilevamento (Recall)
Entrambi i modelli rilevano al 100% le anomalie macroscopiche (Speed Spoofing, Teleport) e progressive (Silent Drift).  
La differenza cruciale emerge negli attacchi semantici più sottili:
| Modello | Detection Rate (Ghost Ship) | Motivo |
| :--- | :--- | :--- |
| **LSTM** | ~59.43% | Varianza alta sui dati normali → Soglia alta ($\tau \approx 0.0276$) → Perde attacchi sottili. |
| **LNN** | ~86.75% | Varianza bassa sui dati normali→ Soglia stretta ($\tau \approx 0.0239$) → Rileva l'anomalia.|

Questo lavoro dimostra che le Liquid Neural Networks rappresentano un passo avanti rispetto alle LSTM per la cybersecurity marittima. Sebbene non "imparino" meglio l'attacco in sé, la loro superiore stabilità nel modellare la dinamica fisica continua permette di definire confini di sicurezza più stretti, riducendo i falsi negativi sugli attacchi più insidiosi
  
## Limite Intrinseco: "Cecità Spaziale"
Un risultato fondamentale dello studio è che entrambi i modelli soffrono di "Cecità Spaziale". Apprendono perfettamente le leggi differenziali del moto (velocità, accelerazione), ma non hanno consapevolezza della geografia assoluta (es. non distinguono terra da mare).

## Conclusione
Questo progetto funge da prova di concetto che le reti neurali liquide, abbinate a principi fisici, offrono una soluzione scalabile e altamente affidabile per la protezione dei sistemi di navigazione da attacchi cinetici.