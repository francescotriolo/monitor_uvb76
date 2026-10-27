import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from funzioni import carica_mono, calcola_inviluppo, calcola_ruvidita, calcola_autocorrelazione, calcola_periodicita, periodicita_nel_tempo, e_anomalo, etichetta_finestra

campioni, fs = carica_mono("buzzer.wav")

durata = len(campioni) / fs

tempo = np.arange(len(campioni)) / fs

inviluppo = calcola_inviluppo(campioni, fs)
finestra = int(0.05 * fs)
tempo_blocchi = np.arange(len(inviluppo)) * (finestra / fs)

ruvidita = calcola_ruvidita(inviluppo)

ac = calcola_autocorrelazione(inviluppo)
ritardi = np.arange(len(ac)) * 0.05

print(calcola_periodicita(inviluppo))

print(periodicita_nel_tempo(inviluppo))