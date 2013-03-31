# -*- coding: utf-8 -*-
from gluon.storage import Storage
# para que os modules criados em \modules sejam lidos
# novamente caso sejam alterados durante a execucao (quando
# a action e acedida, verifica se foram alterados e recarrega-os)
from gluon.custom_import import track_changes;
track_changes(True)
settings = Storage()

# 2013-01-20, AA: Setting utilizado no cliente para saber
# onde guardar os filmes recebidos; deve coincidir com a pasta
# onde esta a pagina apresentada nos outdoors
# settings.movies_path = "c:\\dados\\projectos\\thatsit\\movies"
