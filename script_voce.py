import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from funzioni import carica_mono, calcola_inviluppo, periodicita_nel_tempo, e_anomalo, etichetta_finestra

etichette = [
	(0, 4, "buzzer"),
	(4, 13, "silenzio"),
	(13, 16, "primo callsign (NZhTI)"),
	(16, 19, "secondo callsign"),
	(20, 40, "messaggio"),
	(41, 49, "silenzio"),
	(50, 53, "callsign"),
	(53, 56, "callsign x2"),
	(57, 76, "messaggio"),
	(76, 77, "priyom"),
	(78, 82, "buzzer")
]

campioni, fs = carica_mono("voce.wav")
inviluppo = calcola_inviluppo(campioni, fs)
periodicita = periodicita_nel_tempo(inviluppo, blocchi_per_finestra=200, passo_blocchi=100)


for i, valore in enumerate(periodicita):
	inizio = 5 * i
	nome = etichetta_finestra(inizio, inizio + 10, etichette)
	verdetto = e_anomalo(valore, soglia=0.45)
	print(inizio, round(valore, 2), verdetto, nome)