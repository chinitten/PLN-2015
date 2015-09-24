PLN 2015: Procesamiento de Lenguaje Natural 2015
================================================


Instalación
-----------

1. Se necesita el siguiente software:

   - Git
   - Pip
   - Python 3.4 o posterior
   - TkInter
   - Virtualenv

   En un sistema basado en Debian (como Ubuntu), se puede hacer::

    sudo apt-get install git python-pip python3.4 python3-tk virtualenv

2. Crear y activar un nuevo
   `virtualenv <http://virtualenv.readthedocs.org/en/latest/virtualenv.html>`_.
   Recomiendo usar `virtualenvwrapper
   <http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation>`_.
   Se puede instalar así::

    sudo pip install virtualenvwrapper

   Y luego agregando la siguiente línea al final del archivo ``.bashrc``::

    [[ -s "/usr/local/bin/virtualenvwrapper.sh" ]] && source "/usr/local/bin/virtualenvwrapper.sh"

   Para crear y activar nuestro virtualenv::

    mkvirtualenv --system-site-packages --python=/usr/bin/python3.4 pln-2015

3. Bajar el código::

    git clone https://github.com/PLN-FaMAF/PLN-2015.git

4. Instalarlo::

    cd pln-2015
    pip install -r requirements.txt


Ejecución
---------

1. Activar el entorno virtual con::

    workon pln-2015

2. Correr el script que uno quiera. Por ejemplo::

    python languagemodeling/scripts/train.py -h


Testing
-------

Correr nose::

    nosetests


Chequear Estilo de Código
-------------------------

Correr flake8 sobre el paquete o módulo que se desea chequear. Por ejemplo::

    flake8 languagemodeling

RESULTADOS:

EJERCICIO 3 - GENERACIÓN DE TEXTO.

1 ngram -> [',', ',', ',', '.', 'de', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'el', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', '.', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'la', ',', ',', ',', ',', ',', ',', ',', 'de', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'se', ',', ',', 'de', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'el', ',', ',', ',', ',', ',', ',', 'que', ',', ',', ',', ',', 'que', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'que', ',', ',', ',', ',', ',', 'los', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', 'de', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',', ',']
2 ngram -> ['El', 'coronel', 'Aureliano', ',', 'y', 'se', 'le', 'dijo', 'el', 'coronel', 'Aureliano', 'Buendía', ',', 'en', 'el', 'coronel', 'no', 'se', 'le', 'dijo', '.', 'Y', 'el', 'coronel', 'Aureliano', 'Buendía', '.']
3 ngram -> ['El', 'coronel', 'no', 'supo', 'qué', 'contestar', ',', 'pero', 'no', 'se', 'le', 'ocurrió', 'que', 'tal', 'cosa', 'si', 'de', 'algo', 'que', 'ver', 'todas', 'estas', 'cosas', ',', 'y', 'se', 'fue', 'para', 'él', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'dio', 'tiempo', 'de', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', 'de', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'salvo', 'el', 'reloj', 'de', 'péndulo', 'resonaron', 'en', 'el', 'cuarto', 'de', 'Melquíades', ',', 'en', 'el', 'cuarto', 'de', 'Melquíades', ',', 'y', 'se', 'fue', 'de', 'vacaciones', 'en', 'la', 'casa', ',', 'y', 'se', 'fue', 'a', 'la', 'casa', ',', 'y', 'se', 'fue', ',', 'y', 'se', 'fue', 'a', 'vivir', 'con', 'Meme', '.', 'En', 'el', 'curso', '1949', '.', 'Atribulado', ',', 'recordando', 'el', 'pienso', 'luego', 'existo', '.']
4 ngram -> ['El', 'coronel', 'Aureliano', 'Buendía', ',', 'todavía', 'marcados', 'con', 'la', 'cruz', 'de', 'ceniza', 'en', 'la', 'frente', ',', 'y', 'se', 'fue', 'a', 'visitar', 'al', 'doctor', 'Alirio', 'Noguera', 'para', 'que', 'le', 'devolviera', 'a', 'su', 'esposa', '.']

EJERCICIO 5 - PERPLEXITY (ADDONE)

1 ngram addone -> 1417.2548130685464
2 ngram addone -> 4871.197478051322
3 ngram addone -> 31715.79791493256
4 ngram addone -> 49991.42812360582

EJERCICIO 6 - PREPLEXITY (INTERPOLATED)

1 ngram interpolated -> 1417.2548130685464
2 ngram interpolated -> inf
3 ngram interpolated -> inf
4 ngram interpolated -> inf

EJERCICIO 7 - PREPLEXITY (BACKOFF)

1 ngram backoff -> inf
2 ngram backoff -> inf
3 ngram backoff -> inf
4 ngram backoff -> inf
