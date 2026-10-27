import numpy as np

def blocchi_buzzer_sintetico(n_blocchi, periodo=47):
	for i in range(n_blocchi):
		ampiezza = 1.0 if (i % periodo) < 35 else 0.1
		yield np.full(2400, ampiezza)

def blocchi_rumore(n_blocchi):
	rng = np.random.default_rng(0)
	for _ in range(n_blocchi):
		yield rng.normal(size=2400)

def blocchi_buzzer_rumoroso(n_blocchi, ampiezza_rumore, periodo=47):
	rng = np.random.default_rng(0)
	for blocco in blocchi_buzzer_sintetico(n_blocchi, periodo):
		yield blocco + rng.normal(0, ampiezza_rumore, len(blocco))