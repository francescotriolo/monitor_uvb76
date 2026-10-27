import numpy as np
import soundfile as sf
import pytest
from funzioni import e_anomalo, etichetta_finestra, blocchi_audio

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