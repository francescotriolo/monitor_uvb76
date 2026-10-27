import soundfile as sf
import numpy as np
import csv
import os
from datetime import datetime, timezone
from collections import deque

def carica_mono(percorso):
	campioni, fs = sf.read(percorso)
	if campioni.ndim == 2:
		campioni = campioni[:, 0]
	return campioni, fs	

def calcola_inviluppo(campioni, fs, durata_blocco=0.05):
	finestra = int(durata_blocco * fs)
	n_blocchi = len(campioni) // finestra
	tagliati = campioni[:n_blocchi * finestra]
	blocchi = tagliati.reshape(n_blocchi, finestra)
	inviluppo = np.sqrt(np.mean(blocchi**2, axis=1))
	return inviluppo

def calcola_ruvidita(inviluppo):
	normalizzato = inviluppo / np.mean(inviluppo)
	ruvidita = np.mean(np.abs(np.diff(normalizzato)))
	return ruvidita

def calcola_autocorrelazione(inviluppo):
	x = inviluppo - np.mean(inviluppo)
	ac = np.correlate(x, x, mode="full")
	ac = ac[len(x) - 1:]
	return ac / ac[0]

def calcola_periodicita(inviluppo, durata_blocco=0.05, ritardo_min=1.5, ritardo_max=4.0):
	ac = calcola_autocorrelazione(inviluppo)
	i_min = int(ritardo_min / durata_blocco)
	i_max = int(ritardo_max / durata_blocco)
	zona = ac[i_min:i_max]
	return float(zona.max())

def periodicita_nel_tempo(inviluppo, blocchi_per_finestra=200, passo_blocchi=100):
	risultati = []
	for inizio in range(0, len(inviluppo) - blocchi_per_finestra, passo_blocchi):
		pezzo = inviluppo[inizio : inizio + blocchi_per_finestra]
		periodicita_pezzo = calcola_periodicita(pezzo)
		risultati.append(periodicita_pezzo)
	return risultati

def e_anomalo(periodicita, soglia=0.45):
	return periodicita < soglia

def etichetta_finestra(inizio, fine, etichette):
	migliore = "nessuna"
	sovrapposizione_max = 0
	for (inizio_et, fine_et, nome) in etichette:
		sovrapposizione = max(0, min(fine, fine_et)) - max(inizio, inizio_et)
		if sovrapposizione > sovrapposizione_max:
			sovrapposizione_max = sovrapposizione
			migliore = nome
		elif sovrapposizione == sovrapposizione_max and sovrapposizione > 0:
			migliore = "misto"
	return migliore		

def blocchi_audio(percorso, durata_blocco=0.05):
	fs = sf.info(percorso).samplerate
	dimensione = int(durata_blocco * fs)
	campioni, fs = sf.read(percorso)
	for blocco in sf.blocks(percorso, blocksize=dimensione):
		if len(blocco) < dimensione:
			break
		if blocco.ndim == 2:
			blocco = blocco[:, 0]
		yield blocco

def rms_blocco(blocco):
	return np.sqrt(np.mean(blocco**2))

def periodicita_da_flusso(blocchi, blocchi_per_finestra=200, passo_blocchi=100, durata_blocco=0.05):
	buffer = deque(maxlen=blocchi_per_finestra)
	contatore = 0
	for blocco in blocchi:
		buffer.append(rms_blocco(blocco))
		contatore += 1
		if (contatore - blocchi_per_finestra) % passo_blocchi == 0 and len(buffer) == buffer.maxlen:
			valore = calcola_periodicita(np.array(buffer))
			secondo = (contatore - blocchi_per_finestra) * durata_blocco
			energia = np.mean(buffer)
			yield secondo, valore, energia

def scrivi_riga(percorso, secondo, periodicita, energia):
	nuovo = not os.path.exists(percorso)
	with open(percorso, "a", newline="") as f:
		scrittore = csv.writer(f)
		if nuovo:
			scrittore.writerow(["timestamp", "secondo", "periodicita", "energia"])
		scrittore.writerow([datetime.now(timezone.utc).isoformat(), secondo, periodicita, energia])