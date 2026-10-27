from funzioni import e_anomalo, etichetta_finestra

def test_e_anomalo_sotto_soglia():
	assert e_anomalo(0.03)

def test_e_anomalo_buzzer():
	assert not e_anomalo(0.68)

def test_finestra_dominata_dal_silenzio():
	etichette = [(0, 4, "buzzer"), (4, 13, "silenzio"), (13, 16, "callsign")]
	assert etichetta_finestra(0, 10, etichette) == "silenzio"

def test_etichetta_fuori():
	etichette = [(0, 4, "buzzer"), (4, 13, "silenzio")]
	assert etichetta_finestra(100, 110, etichette) == "nessuna"

def test_vince_la_sovrapposizione_maggiore_dopo_un_pareggio():
	etichette = [(0, 3, "a"), (3, 6, "b"), (6, 10, "c")]
	assert etichetta_finestra(0, 10, etichette) == "c"