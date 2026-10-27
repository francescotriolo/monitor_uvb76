from funzioni import periodicita_da_flusso, blocchi_audio, scrivi_riga
from segnali_sintetici import blocchi_buzzer_sintetico, blocchi_rumore

for secondo, valore, energia in periodicita_da_flusso(blocchi_buzzer_sintetico(400)):
	print("buzzer", secondo, valore, energia)
	scrivi_riga("log_prova.csv", secondo, valore, energia)

for secondo, valore, energia in periodicita_da_flusso(blocchi_rumore(400)):
	print("rumore", secondo, valore, energia)
	scrivi_riga("log_prova.csv", secondo, valore, energia)
