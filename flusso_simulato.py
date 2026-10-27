from funzioni import periodicita_da_flusso, blocchi_audio

for secondo, valore in periodicita_da_flusso(blocchi_audio("voce.wav")):
	print(secondo, valore)

