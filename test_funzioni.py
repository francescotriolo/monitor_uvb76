import numpy as np
import soundfile as sf
import pytest
from funzioni import e_anomalo, etichetta_finestra, blocchi_audio, periodicita_da_flusso, rms_blocco, scrivi_riga, classifica_finestra

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

def test_blocchi_stereo_diventano_mono(tmp_path):
	percorso = str(tmp_path / "stereo.wav")
	sf.write(percorso, np.zeros((4800, 2)), 48000)

	blocchi  = list(blocchi_audio(percorso))

	assert len(blocchi) == 2
	assert blocchi[0].ndim == 1

def test_ultimo_blocco_incompleto_scartato(tmp_path):
	percorso = str(tmp_path / "stereo.wav")
	sf.write(percorso, np.zeros((5000, 2)), 50000)

	blocchi = list(blocchi_audio(percorso))

	assert len(blocchi) == 2
	assert blocchi[0].ndim == 1

def test_rms_blocco_costante():
	assert rms_blocco(np.full(100, 0.5)) == pytest.approx(0.5)

def blocchi_buzzer_sintetico(n_blocchi, periodo=47):
	for i in range(n_blocchi):
		ampiezza = 1.0 if (i % periodo) < 35 else 0.1
		yield np.full(2400, ampiezza)

def blocchi_rumore(n_blocchi):
	rng = np.random.default_rng(0)
	for _ in range(n_blocchi):
		yield rng.normal(size=2400)

def test_buzzer_sintetico_e_periodico():
	valori = [v for _, v, _ in periodicita_da_flusso(blocchi_buzzer_sintetico(400))]
	assert len(valori) == 3
	assert all(v > 0.45 for v in valori), valori

def blocchi_buzzer_rumoroso(n_blocchi, ampiezza_rumore, periodo=47):
	rng = np.random.default_rng(0)
	for blocco in blocchi_buzzer_sintetico(n_blocchi, periodo):
		yield blocco + rng.normal(0, ampiezza_rumore, len(blocco))

def test_scrivi_riga(tmp_path):
	percorso = str(tmp_path / "log.csv")
	scrivi_riga(percorso, 0.0, 0.5, 0.1)
	scrivi_riga(percorso, 5.0, 0.4, 0.1)
	with open(percorso) as f:
		righe = f.readlines()
	assert len(righe) == 3

def test_classifica_finestra():
	assert classifica_finestra(float("nan"), 0.0) == "nessun segnale"