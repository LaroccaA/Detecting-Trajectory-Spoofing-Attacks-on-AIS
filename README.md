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

## Metodologia di Rilevamento: Physics-Informed Dual-Threshold

Per classificare le anomalie in modo affidabile, il sistema utilizza un approccio a due giudici basato sulla navigazione reale:

1.  **Ricostruzione Fisica (Dead Reckoning):** L'Autoencoder viene utilizzato per predire i parametri dinamici (SOG e COG). Questi sono poi reintrodotti in formule di navigazione per ricalcolare la posizione futura della nave.
2.  **Score Dinamico:** Misura l'incoerenza del movimento (errore su SOG/COG).
3.  **Score Fisico:** Misura l'incoerenza spaziale (la distanza tra la posizione GPS *reale* e la posizione *calcolata* fisicamente).

L'allarme scatta se **entrambe** le componenti dinamiche o fisiche superano la loro soglia specifica, calcolata statisticamente con la **Regola del 3-Sigma ($\mu + 3\sigma$)**.

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