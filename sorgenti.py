import time
from funzioni import calcola_attesa

def sorgente_con_riconnessione(apri_sorgente, attendi=time.sleep):
	tentativo = 0
	while True:
		letti = 0
		try:
			for blocco in apri_sorgente():
				letti += 1
				if letti == 100:
					tentativo = 0
				yield blocco
		except ConnectionError:
			pass
		yield None
		attendi(calcola_attesa(tentativo))
		tentativo += 1