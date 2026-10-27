from funzioni import e_anomalo, etichetta_finestra

def test_e_anomalo_sotto_soglia():
	assert e_anomalo(0.03)

def test_e_anomalo_buzzer():
	assert not e_anomalo(0.68)

def test_finestra_dominata_dal_silenzio():
	etichette = [(0, 4, "buzzer"), (4, 13, "silenzio"), (13, 16, "callsign")]
	assert etichetta_finestra(0, 10, etichette) == "silenzio"