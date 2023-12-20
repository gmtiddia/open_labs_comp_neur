Istruzioni
==========

Vi chiediamo di seguire queste istruzioni **prima** dell'inizio del laboratorio.

.. note::
    Per qualunque problema relativo all'installazione dei software necessari contattate
    Gianmarco Tiddia all'inidrizzo gianmarco.tiddia@dsf.unica.it.

Installazione del simulatore NEST
+++++++++++++++++++++++++++++++++

Per installare il simulatore NEST si può procedere in svariati modi, indicati 
nella `documentazione del simulatore <https://nest-simulator.readthedocs.io/en/latest/installation/index.html>`_.

Per questo laboratorio consigliamo di procedere con l'installazione di una macchina virtuale.

In primo luogo avrete bisogno di `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_. 
Potete seguire le istruzioni indicate sulla pagina del software per poterlo installare nel vostro computer.

.. note::
    Gli utenti macOS provvisti di macchina con chip non Intel non possono utilizzare VirtualBox. Si chiede, in questo caso, di
    installare `Homebrew <https://brew.sh/>`_ e successivamente NEST utilizzando il comando

    .. code-block:: bash
        brew install nest
    
    Una volta fatto ciò potete utilizzare NEST semplicemente importandolo come pacchetto Python. Potete passare alla sezione successiva!

Una volta installato VirtualBox, potete scaricare la macchina virtuale contenente NEST `a questo link <https://nest-simulator.org/downloads/gplreleases/nest-latest.ova>`_.
Potete seguire le istruzioni indicate `qui <https://nest-simulator.readthedocs.io/en/latest/installation/livemedia.html#download-the-nest-image-for-vms>`_
per importare la macchina virtuale su VirtualBox per poi lanciare NEST. La password richiesta per poter accedere è **nest**.

Correttezza installazione
+++++++++++++++++++++++++

Una volta avviata la macchina virtuale o installato NEST, potete controllare che l'installazione sia andata a buon fine.
Per fare questo dovrete aprire un terminale. Digitate

.. code-block:: bash
    wget https://nest-simulator.readthedocs.io/en/stable/_downloads/63da57de96edd7f5c560300061e00c00/one_neuron.py

e successivamente

.. code-block:: bash
    python one_neuron.py

Il risultato finale dovrebbe essere un grafico indicante l'andamento del potenziale di membrana di un neurone.
