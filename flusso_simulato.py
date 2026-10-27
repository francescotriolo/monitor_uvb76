import numpy as np
from collections import deque
from funzioni import blocchi_audio, rms_blocco, calcola_periodicita

BLOCCHI_PER_FINESTRA = 200
PASSO_BLOCCHI = 100

buffer = deque(maxlen=BLOCCHI_PER_FINESTRA)
contatore = 0
risultati = []

for blocco in blocchi_audio("voce.wav"):
	buffer.append(rms_blocco(blocco))
	contatore += 1

	if (contatore - BLOCCHI_PER_FINESTRA) % PASSO_BLOCCHI == 0 and len(buffer) == buffer.maxlen:
		valore = calcola_periodicita(np.array(buffer))
		risultati.append(valore)
		print((contatore - BLOCCHI_PER_FINESTRA) * 0.05)
		print(valore)
