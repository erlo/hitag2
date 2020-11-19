# Hitag2

Ressources décrites dans l'article MISC sur l'exploration de Hitag2

Liste des fichiers:

* `capture.grc`: Capture du signal émis par une clé de voiture pour l'envoyer sur une socket UDP
* `transmit.grc`: Transmission d'un signal dont les symboles sont définis dans `/tmp/frametosend`
* `udp_server_hitag.py`: Serveur UDP permettant de récupérer les données capturées par GRC, et décode les trames.
* `recoverkey.c`: Calcul l'ensemble des valeurs possibles du LFSR pour un Keystream. (A compiler depuis le Makefile) [Source: <https://github.com/factoritbv/hitag2hell>]
* `checkLFSR.sh`: Permet d'identifier le LFSR correspondant aux Keystream à partir de 2 captures
* `hitag2_get_equivkey.py`: Calcul la clé Hitag2 équivalente [Source: <https://github.com/factoritbv/hitag2hell>]
* `hitag2.py`: Implémentation de l'algorithme Hitag2 [Source: <https://github.com/factoritbv/hitag2hell>]
* `generate_frame.py`: Génère tous les symboles d'une transmission (Suite de 0 et de 1 sur la sortie standard)
