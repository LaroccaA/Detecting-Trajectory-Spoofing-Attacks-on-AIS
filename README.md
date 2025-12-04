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

## Metodologia di Rilevamento: Statistical MAE Thresholding ($3\sigma$)

Il sistema di rilevamento degli errori è stato impostato sul calcolo e l'analisi del Mean Absolute Error (MAE) di ricostruzione, con la soglia di allarme definita statisticamente tramite la Regola dei $3\sigma$ sui dati normali.Questa scelta metodologica si basa sull'analisi della distribuzione degli errori generati dai modelli (LSTM e LNN) su traffico lecito. Il sistema di allarme si affida interamente a un confine statistico rigoroso:

   * **Definizione Statistica della Soglia:** Regola della Deviazione Standard ($\mathbf{3\sigma}$). La soglia viene calcolata prendendo come riferimento solo i dati normali, stabilendo un limite oltre il quale l'errore è considerato anomalo:$$Threshold = \mu_{normale} + 3\sigma_{normale}$$

   * **Calcolo:** La soglia è definita come la Media ($\mu$) degli errori di ricostruzione sui dati normali, più tre volte la loro Deviazione Standard ($\sigma$).
   
   * **Funzionamento:** Questo approccio robusto garantisce che il limite sia posizionato in modo da coprire statisticamente il 99.7% dei comportamenti leciti, garantendo al contempo un bassissimo tasso di falsi positivi.

   * Sistema di Allarme Binario: La classificazione è semplice e immediata:$$\text{Alert} = (\text{MAE} > \text{Threshold})$$

***

## 📁 Struttura del Repository

Il progetto è organizzato per funzionalità, con cartelle dedicate a ciascun modello e a ciascun tipo di test:

| Cartella / File | Contenuto e Scopo |
| :--- | :--- |
| `Progetto/LNN_V2/LNN.ipynb` | **Training Principale:** Addestramento e configurazione avanzata dell'Autoencoder LNN. |
| `Progetto/LNN_V2/Test.ipynb` | **Test Quantitativo & Qualitativo LNN:** Calibrazione delle soglie e validazione generale delle performance. |
| `Progetto/LNN_V2/Test_Kinematic_Inconcistency.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Teletrasporto** (salto GPS impossibile). |
| `Progetto/LNN_V2/Test_Silent_Drift.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Silent Drift** (deriva lenta e insidiosa). |
| `Progetto/LSMT_V2/LSMT.ipynb` | **Training Principale:** Addestramento e configurazione avanzata dell'Autoencoder LSMT. |
| `Progetto/LSMT_V2/Test.ipynb` | **Test Quantitativo & Qualitativo LSMT:** Calibrazione delle soglie e validazione generale delle performance. |
| `Progetto/LSMT_V2/Test_Kinematic_Inconcistency.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Teletrasporto** (salto GPS impossibile). |
| `Progetto/LSMT_V2/Test_Silent_Drift.ipynb` | **Test Focalizzato:** Simulazione e analisi del rilevamento dell'attacco **Silent Drift** (deriva lenta e insidiosa). |
| `Progetto/Pre-Elaborazione Dati/` | Contiene gli script di pulizia dati (es. `Pulizia Data AIS.ipynb`) e lo **`scaler.joblib`** per la normalizzazione. |

***
## Conclusione
Questo progetto funge da prova di concetto che le reti neurali liquide, abbinate a principi fisici, offrono una soluzione scalabile e altamente affidabile per la protezione dei sistemi di navigazione da attacchi cinetici.