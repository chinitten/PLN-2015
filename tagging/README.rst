Resultados:
-----------

Ejercicio 1 - Estadísticas de etiquetas POS
-------------------------------------------

sents:: 17379
words:: 517268
vocabulary:: 46482
tags:: 48

tag	frequency	%	most5

nc	92002	17.79%	('años', 'presidente', 'millones', 'equipo', 'partido')

sp	79904	15.45%	('de', 'en', 'a', 'del', 'con')

da	54552	10.55%	('la', 'el', 'los', 'las', 'El')

vm	50609	9.78%	('está', 'tiene', 'dijo', 'puede', 'hace')

aq	33904	6.55%	('pasado', 'gran', 'mayor', 'nuevo', 'próximo')

fc	30148	5.83%	(',',)

np	29113	5.63%	('Gobierno', 'España', 'PP', 'Barcelona', 'Madrid')

fp	21157	4.09%	('.', '(', ')')

rg	15333	2.96%	('más', 'hoy', 'también', 'ayer', 'ya')

cc	15023	2.90%	('y', 'pero', 'o', 'Pero', 'e')

n	words	%	examples

1	44109	94.89%	[(',', 30148), ('el', 14524), ('en', 12114), ('con', 4150), ('por', 4087)]

2	2194	4.72%	[('la', 18100), ('y', 11212), ('"', 9296), ('los', 7824), ('del', 6519)]

3	153	0.33%	[('.', 17520), ('a', 8200), ('un', 5198), ('no', 3300), ('es', 2315)]

4	19	0.04%	[('de', 28478), ('dos', 917), ('este', 830), ('tres', 425), ('todo', 393)]

5	4	0.01%	[('que', 15391), ('mismo', 247), ('cinco', 224), ('medio', 105)]

6	3	0.01%	[('una', 3852), ('como', 1736), ('uno', 335)]

Descripción de etiquetas.

nc: Nombre común.
sp: Preposición.
da: Artículo.
vm: Verbo principal.
aq: Adjetivo calificativo.
fc: Coma.
np: Nombre propio.
fp: Punto.
rg: Adverbio General.
cc: Conjunción Coordinada.


Ejercicio 3 - Entrenamiento y Evaluación de Taggers
---------------------------------------------------

Accuracy:: 89.00%

Known Accuracy:: 95.31%

Unknown Accuracy:: 31.80%

Time::
real	0m2.367s
user	0m2.312s
sys	0m0.056s


Ejercicio 5 - HMM POS Tagger
----------------------------

n:: 1

Accuracy:: 89.03%

Known Accuracy:: 95.34%

Unknown Accuracy:: 31.80%

Time::
real	0m10.663s
user	0m9.892s
sys	0m0.076s

n:: 2

Accuracy:: 92.61%

Known Accuracy:: 97.44%

Unknown Accuracy:: 48.81%


Time::
real	0m43.166s
user	0m43.132s
sys	0m0.048s

n:: 3

Accuracy:: 92.52%

Known Accuracy:: 96.98%

Unknown Accuracy:: 52.18%

Time::
real	3m36.039s
user	3m36.060s
sys	0m0.088s

n:: 4

Accuracy:: 92.42%

Known Accuracy:: 96.69%

Unknown Accuracy:: 53.76%

Time::
real	17m40.007s
user	17m40.012s
sys	0m0.444s

Ejercicio 7 - Maximum Entropy Markov Models
-------------------------------------------

LogisticRegression::

n:: 1

Accuracy:: 92.69%

Known Accuracy:: 95.27%

Unknown Accuracy:: 69.31%

Time::
real	0m25.190s
user	0m24.640s
sys	0m0.104s

n:: 2

Accuracy:: 89.73%

Known Accuracy:: 93.30%

Unknown Accuracy:: 57.32%

Time::
real	0m49.869s
user	0m49.784s
sys	0m0.096s

n:: 3

Accuracy:: 89.83%

Known Accuracy:: 93.48%

Unknown Accuracy:: 56.76%

Time::
real	1m5.271s
user	1m5.204s
sys	0m0.088s

n::4

Accuracy:: 90.87%

Known Accuracy:: 93.97%

Unknown Accuracy:: 62.74%

Time::
real	1m21.729s
user	1m21.648s
sys	0m0.112s

LinearSVC::

n:: 1

Accuracy:: 94.43%

Known Accuracy:: 97.04%

Unknown Accuracy:: 70.82%

real	0m24.858s
user	0m24.740s
sys	0m0.116s

n:: 2

Accuracy:: 91.55%

Known Accuracy:: 95.62%

Unknown Accuracy:: 54.62%

real	0m49.402s
user	0m48.856s
sys	0m0.104s

n:: 3

Accuracy:: 92.11%

Known Accuracy:: 95.82%

Unknown Accuracy:: 58.47%

real	1m10.607s
user	1m10.044s
sys	0m0.108s

n:: 4

Accuracy:: 92.94%

Known Accuracy:: 96.09%

Unknown Accuracy:: 64.38%

real	1m20.871s
user	1m20.792s
sys	0m0.108s

MultinomialNB::

n:: 1

Accuracy:: 78.84%

Known Accuracy:: 82.12%

Unknown Accuracy:: 49.09%

real	15m38.776s
user	15m39.104s
sys	0m0.180s

n:: 2

Accuracy:: 84.36%

Known Accuracy:: 87.95%

Unknown Accuracy:: 51.87%

real	16m29.793s
user	16m30.160s
sys	0m0.168s

n:: 3

Accuracy:: 84.17%

Known Accuracy:: 87.74%

Unknown Accuracy:: 51.79%

real	18m32.846s
user	18m33.216s
sys	0m0.192s

n:: 4

Accuracy:: 82.63%

Known Accuracy:: 86.14%

Unknown Accuracy:: 50.80%

real	38m45.800s
user	23m49.056s
sys	14m57.916s
