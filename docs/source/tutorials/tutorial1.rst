Tutorial 1: simulazione di un singolo neurone
=============================================

Il simulatore NEST può essere utilizzato come un comune pacchetto Python.
Qui vediamo un semplice esempio nel quale un singolo neurone è soggetto a
una corrente costante.


Creiamo i nodi
--------------

Una rete neurale simulata su NEST sarà composta di due elementi base: i **nodi** e le **connessioni**.
I nodi possono essere neuroni o dispositivi, come generatori di segnali di vario tipo, o 
nodi che registrano i valori di potenziale di membrana o i tempi di emissione degli spikes.

Per creare un nodo è sufficiente chiamare il comando *Create*,
che prende in entrata il nome del modello che vogliamo creare e altri parametri opzionali.

Per questo tutorial dobbiamo importare NEST e Matplotlib, per cui digitiamo:

.. code-block:: python

    import matplotlib.pyplot as plt
    import nest

Ora creiamo il nostro neurone, digitando

.. code-block:: python

    neuron = nest.Create("iaf_psc_alpha")

dove "iaf_psc_alpha" non è altro che il nome del modello di neurone che vogliamo simulare.
A questo punto il neurone verrà creato con i suoi parametri di default. Tra questi c'è un 
parametro, chiamato *I_e*, che indica un valore di corrente di fondo (in pA).
Per fare emettere dei segnali al neurone ci basta modificare questo parametro, che di default
assume valore 0 pA.

Per fare questa modifica possiamo digitare:

.. code-block:: python

    neuron.set({"I_e": 376})

Che imposta il valore di corrente di fondo a 376.0 pA.

NB ci sono diversi modi per modificare i parametri di un nodo. Uno alternativo, ad esempio, si
può attuare chiamando il comando *SetStatus* nel modo seguente:

.. code-block:: python

    nest.SetStatus(neuron, {"I_e": 376.0})

Che imposta il valore di corrente di 376.0 pA al nodo chiamato *neuron*.
A questo punto possiamo procedere con la creazione del dispositivo che registrerà il potenziale elettrico di 
membrana del neurone, che si chiama, appunto, *multimeter*. Il dispositivo è in grado, come quello vero, di 
registrare non solo i valori di potenziale elettrico, ma anche quelli di corrente.

Digitiamo dunque:

.. code-block:: python

    multimeter = nest.Create("multimeter")
    multimeter.set(record_from=["V_m"])

In questo modo il multimetro registrerà solo il potenziale di membrana del neurone (*V_m*).

Creiamo adesso un altro nodo, in grado di registrare gli spikes emessi da un neurone, ovvero lo *spike_recorder*.

.. code-block:: python

    spikerecorder = nest.Create("spike_recorder")


A questo punto possiamo procedere connettendo i nodi tra loro!

Connettiamo i nodi
------------------

Per connettere due nodi tra loro si usa il comando *Connect*, che prende in ingresso due nodi.
Nel nostro caso dobbiamo connettere il multimetro al neurone, e il neurone allo spike_recorder:

.. code-block:: python

    nest.Connect(multimeter, neuron)
    nest.Connect(neuron, spikerecorder)

La connessione va intesa "da sinistra verso destra", ovvero il primo nodo si connette al secondo. 
Per cui, se due neuroni (1 e 2) dovessero essere connessi tra loro, il neurone 2 verrà stimolato dal neurone 1, e non vice versa.
In questo caso, il multimetro invia al neurone la richiesta di "lettura" del potenziale di membrana, mentre il neurone invia il suo segnale in uscita,
ovvero gli spikes, allo spike recorder.

A questo punto dobbiamo simulare la rete che abbiamo appena creato. Dobbiamo dire a NEST per quanto tempo (in ms) dobbiamo
simulare questa rete. Supponiamo di voler simulare un secondo di attività. Basterà digitare:

.. code-block:: python

    nest.Simulate(1000.0)


Estrarre i dati e metterli in un grafico
----------------------------------------

Una volta completata la simulazione, vediamo cosa ha registrato il multimetro.
Dobbiamo raccogliere non solo il potenziale di membrana registrato, ma anche gli 
sitanti temporali ai quali il multimetro ha registrato quei valori.

Per fare questo digitiamo:

.. code-block:: python

    dmm = multimeter.get()
    Vms = dmm["events"]["V_m"]
    ts = dmm["events"]["times"]

Dove *Vms* raccoglie i potenziali di membrana e *ts* i tempi.

A questo punto facciamo un plot del potenziale di membrana usando Matplotlib.

.. code-block:: python

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.plot(ts, Vms)
    plt.draw()

Ora facciamo la stessa cosa per lo spike recorder, creando un secondo plot.

.. code-block:: python

    # estrazione dati spike recorder
    events = spikerecorder.get("events")
    senders = events["senders"]
    ts = events["times"]

    # grafico
    plt.figure(2)
    plt.plot(ts, senders, ".")
    plt.show()

Ed ecco i risultati della simulazione!
