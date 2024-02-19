"""
Rete bilanciata simulata con NEST
---------------------------------

Questo scripyt è basato sull'esempio di NEST chiamato brunel_alpha_nest.py e 
adattato per gli Open Labs del gruppo di Neuroscienza Computazionale 
dell'Università di Cagliari.

"""

###############################################################################
# Importiamo i moduli necessari per fare la simulazione.

import time
import numpy as np
import scipy.special as sp
import nest
import nest.raster_plot
import matplotlib.pyplot as plt


###############################################################################
# Definiamo le funzioni usate nell'esempio. Non ci serve analizzarle nel 
# dettaglio, per i nostri scopi è sufficiente definirle.

def LambertWm1(x):
    # Using scipy to mimic the gsl_sf_lambert_Wm1 function.
    return sp.lambertw(x, k=-1 if x < 0 else 0).real

def ComputePSPnorm(tauMem, CMem, tauSyn):
    a = (tauMem / tauSyn)
    b = (1.0 / tauSyn - 1.0 / tauMem)

    # time of maximum
    t_max = 1.0 / b * (-LambertWm1(-np.exp(-1.0 / a) / a) - 1.0 / a)

    # maximum of PSP for current of unit amplitude
    return (np.exp(1.0) / (tauSyn * CMem * b) *
            ((np.exp(-t_max / tauMem) - np.exp(-t_max / tauSyn)) / b -
             t_max * np.exp(-t_max / tauSyn)))




###############################################################################
# Iniziamo a far partire la simulazione! È buona norma resettare sempre il
# kernel del simulatore prima.

nest.ResetKernel()

# facciamo partire un timer. Ci servirà per capire quanto tempo si impiega a
# costruire la rete
startbuild = time.time()


###############################################################################
# Definiamo alcuni parametri temporali importanti

dt = 0.1    # la risoluzione della simulazione (in ms)
simtime = 1000.0  # tempo biologico simulato (in ms)
delay = 1.5    # delay delle sinapsi (in ms)

###############################################################################
# Definizione di parametri che sono findamentali per garantire un'attività
# realistica per il nostro modello.

g = 5.0  # rappprto tra i pesi inhibitori ed eccitatori
eta = 2.0  # rate dello stimolo esterno
epsilon = 0.1  # probabilità di connessione

###############################################################################
# Definiamo il numero di neuroni della rete e il sottoinsieme dei neuroni da
# cui misuriamo i segnali.

order = 2500
NE = 4 * order  # numero di neuroni eccitatori
NI = 1 * order  # numero di neuroni inibitori
N_neurons = NE + NI   # numero totale di neuroni
N_rec = 50      # numero di neuroni da cui registriamo i segnali

###############################################################################
# Parametri di connettività. Definiamo quante connessioni ha ciascun neurone
# e di che tipo sono (eccitatorie o inibitorie)

CE = int(epsilon * NE)  # numero di connessioni eccitatorie per neurone
CI = int(epsilon * NI)  # numero di connessioni inibitorie per neurone
C_tot = int(CI + CE)      # numero totale di connessioni per neurone

###############################################################################
# Inizializziamo i parametri del neurone LIF e delle sinapsi. Questi parametri
# vengono inseriti in dizionari Python e le correnti sinaptiche sono
# regolate in modo che abbiano, come effetto, un determinato aumento del
# potenziale di membrana sul neurone ricevente. Per gli scopi del
# tutorial, questa spiegazione è più che sufficiente :)

tauSyn = 0.5  # costante tempo della sinapsi (in ms)
tauMem = 20.0  # costante tempo della membrana del neurone (in ms)
CMem = 250.0  # capacità della membrana (in pF)
theta = 20.0  # potenziale di soglia della membrana (in mV)
neuron_params = {"C_m": CMem,
                 "tau_m": tauMem,
                 "tau_syn_ex": tauSyn,
                 "tau_syn_in": tauSyn,
                 "t_ref": 2.0,
                 "E_L": 0.0,
                 "V_reset": 0.0,
                 "V_m": 0.0,
                 "V_th": theta}
J = 0.1        # ampiezza del potenziale postsinaptico (o PSP) (in mV)
J_unit = ComputePSPnorm(tauMem, CMem, tauSyn)
J_ex = J / J_unit  # ampiezza del PSP eccitatorio
J_in = -g * J_ex    # ampiezza del PSP inibitorio

###############################################################################
# Queste righe ci dicono che rate assegnare all'input esterno in modo che
# i neuroni della nostra rete assumano un certo firing rate.

nu_th = (theta * CMem) / (J_ex * CE * np.exp(1) * tauMem * tauSyn)
nu_ex = eta * nu_th
p_rate = 1000.0 * nu_ex * CE

################################################################################
# Configuriamo il kernel della simulazione di NEST, specificando la risoluzione
# temporale e alcuni parametri secondari.

nest.resolution = dt
nest.print_time = True
nest.overwrite_files = True

print("Costruzione della rete")

###############################################################################
# Creiamo i neuroni e tutto il necessario usando il comando ``Create``. 
# In particolare creiamo i neuroni eccitatori, quelli inibitori,
# il segnale esterno e dei recorder, il cui scopo è quello di registrare i
# segnali emessi dai neuroni a cui sono connessi.

nodes_ex = nest.Create("iaf_psc_alpha", NE, params=neuron_params)
nodes_in = nest.Create("iaf_psc_alpha", NI, params=neuron_params)
noise = nest.Create("poisson_generator", params={"rate": p_rate})
espikes = nest.Create("spike_recorder")
ispikes = nest.Create("spike_recorder")

###############################################################################
# Definiamo una sinapsi statica, ovvero un tipo di sinapsi il cui peso non
# cambia nel tempo. Prepariamo sinapsi eccitatorie e inibitorie, che avranno
# un peso differente. Questi comandi servono per evitare di fornire queste 
# informazioni a ogni chiamata di connessione.

nest.CopyModel("static_synapse", "excitatory",
               {"weight": J_ex, "delay": delay})
nest.CopyModel("static_synapse", "inhibitory",
               {"weight": J_in, "delay": delay})

#################################################################################
# Ora connettiamo il segnale esterno (noise) a tutti i neuroni della rete,
# utilizzando una sinapsi di tipo eccitatorio.

nest.Connect(noise, nodes_ex, syn_spec="excitatory")
nest.Connect(noise, nodes_in, syn_spec="excitatory")

###############################################################################
# Connettiamo i primi ``N_rec`` neuroni eccitatori e inibitori ai recorder in
# modo da registrarne gli spikes.

nest.Connect(nodes_ex[:N_rec], espikes, syn_spec="excitatory")
nest.Connect(nodes_in[:N_rec], ispikes, syn_spec="excitatory")

###############################################################################
# Creiamo le connessioni eccitatorie tra i neuroni della rete. Le connessioni
# di questo tipo "partiranno" da neuroni eccitatori (nodes_ex) e "arriveranno"
# a tutti i neuroni del modello (nodes_ex + nodes_in). La regola di connessione
# assegna a ciascun neurone CE connessioni in ingresso, e sceglie a caso i 
# neuroni presinaptici prendendo dalla popolazione nodes_ex.


conn_params_ex = {'rule': 'fixed_indegree', 'indegree': CE}
nest.Connect(nodes_ex, nodes_ex + nodes_in, conn_params_ex, "excitatory")

###############################################################################
# Facciamo la stessa cosa ma con le connessioni inibitorie.

conn_params_in = {'rule': 'fixed_indegree', 'indegree': CI}
nest.Connect(nodes_in, nodes_ex + nodes_in, conn_params_in, "inhibitory")

###############################################################################
# Registriamo il tempo, così da misurare quanto abbiamo impiegato a costruire
# la rete.

endbuild = time.time()

###############################################################################
# Simuliamo la dinamica neuronale!

print("Simulazione della rete")

nest.Simulate(simtime)

###############################################################################
# Registriamo il tempo così da capire quanto abbiamo impiegato a simulare la
# dinamica.

endsimulate = time.time()

###############################################################################
# Raccogliamo gli spikes che saranno stati registrati dagli spike recorder.

events_ex = espikes.n_events
events_in = ispikes.n_events

###############################################################################
# Calcoliamo il firing rate medio per ciascuna popolazione di neuroni. La
# misura finale sarà in Hz (1Hz = 1 spike/s per ciascun neurone).

rate_ex = events_ex / simtime * 1000.0 / N_rec
rate_in = events_in / simtime * 1000.0 / N_rec

###############################################################################
# Misuriamo i due timer fondamentali quando facciamo simulazioni di SNN:
# il tempo di costruzione della rete e il tempo della simulazione della
# dinamica neuronale.

build_time = endbuild - startbuild
sim_time = endsimulate - endbuild

###############################################################################
# Facciamo dei print di riepilogo.

print("Riepilogo della simulazione")
print(f"Numero di neuroni   : {N_neurons}")
print(f"Connessioni E totali: {int(CE * N_neurons) + N_neurons}")
print(f"Connessioni I totali: {int(CI * N_neurons)}")
print(f"Rate eccitatorio    : {rate_ex:.2f} Hz")
print(f"Rate inibitorio     : {rate_in:.2f} Hz")
print(f"Tempo di costruzione: {build_time:.2f} s")
print(f"Tempo di simulazione: {sim_time:.2f} s")

###############################################################################
# Facciamo un plot di riepilogo.

nest.raster_plot.from_device(espikes, hist=True, title="Neuroni eccitatori")
#nest.raster_plot.from_device(ispikes, hist=True, title="Neuroni inibitori")
plt.show()
