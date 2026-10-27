from funzioni import periodicita_da_flusso, blocchi_audio

for secondo, valore in periodicita_da_flusso(blocchi_buzzer_sintetico(400)):
	print("buzzer", secondo, valore)

for secondo, valore in periodicita_da_flusso(blocchi_rumore(400)):
	print("rumore", secondo, valore)