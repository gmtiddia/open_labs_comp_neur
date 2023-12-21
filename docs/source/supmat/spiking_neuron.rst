Com'è fatto un neurone spiking
==============================

Generalità
++++++++++

Un neurone spiking è un neurone puntiforme caratterizzato da una variabile di stato: il potenziale elettrico della membrana.

Infatti, i neuroni comunicano tra loro per mezzo di impulsi elettrici, e quindi al loro interno hanno luogo
dei meccanismi che portano a un cambiamento delle concentrazioni ioniche tra l'interno e l'esterno della membrana.
Nel caso di un neurone a riposo, le differenti concentrazioni di ioni tra l'interno e l'esterno della membrana portano 
a una differenza di potenziale elettrico tra il citosol e lo spazio extracellulare pari a -70 mV. 

Sappiamo inoltre che la membrana di un neurone, così come quella di tutte le cellule del nostro organismo, ha dei *canali*,
che permettono il passaggio delle sostanze nutritive. Esistono poi tutta una serie di *canali ionici*, in grado di trasportare
determinati ioni all'interno o all'esterno del neurone, sia secondo gradiente di concentrazione che contro gradiente.
Capiamo quindi che la concentrazione delle specie ioniche può cambiare nel tempo, e quindi anche il potenziale di membrana.

Ora abbiamo tutti gli ingredienti per capire come funziona il neurone spiking più semplice in assoluto: il Leaky Integrate-and-Fire,
detto anche LIF.

Il neurone LIF
++++++++++++++

Il neurone LIF è un modellino fenomenologico che considera tutte le osservazioni fatte in precedenza per costruire un modello
semplice, ma allo stesso tempo con un buon potere predittivo e "leggero" da simulare, cosa importantissima quando si vanno
a creare reti con milioni di neuroni.

In primis il neurone ha un potenziale di membrana in quanto la sua membrana, impermeabile, separa zone con diverse concentrazioni
ioniche (prevalentemente ioni negativi all'interno del neurone e positivi all'esterno). Le conoscenze di Fisica 2 ci permettono
quindi di immaginare la membrana come una sorta di condensatore, dotato di una certa capacità!

Allo stesso modo, la membrana è provvista di diversi canali ionici, che permettono il passaggio di cariche, ovvero ioni, tra
l'interno e l'esterno della cellula. In questo senso, possiamo immaginare i canali come delle resistenze!

A questo punto, unendo queste osservazioni, possiamo pensare a un neurone come a un circuito RC!
Tuttavia, un neurone spiking emette spikes, ma sappiamo bene che un circuito RC non può fare una cosa del genere.

Nei neuroni biologici, è stato osservato che, quando il potenziale di membrana raggiunge un valore critico (circa -55 mV),
viene innescato un meccanismo per cui, in modo non lineare, il potenziale di membrana aumenta per un breve periodo garantendo
quello che noi chiamiamo spike (o potenziale d'azione). Nel nostro modellino, possiamo quindi introdurre un potenziale di
soglia, per cui al superamento della soglia viene innescato il meccanismo di emissione del segnale.

Quindi, in ultima analisi, il neurone LIF è interamente descritto dall'equazione differenziale lineare del circuito RC accoppiata
a un semplice meccanismo di soglia. Una volta superata la soglia, il potenziale di membrana viene riportato a un valore vicino a 
quello di riposo per emulare il comportamento dei neuroni biologici subito dopo l'emissione dello spike.

Nel tutorial che vedremo, andremo a simulare un gruppo di neuroni di questo tipo.


