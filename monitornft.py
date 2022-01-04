# 
#
# struttura del programma
#   1) fornire un wallet address da analizzare 
#       (decidere dove memorizzarlo :
#           a) all'interno del codice in un primo momento
#           b) in un file txt
# 
#   2) leggere tutti gli NFT associati a quel wallet address
#   
#   3) memorizzare i risultati
#       OKKIO: per evitare ogni volta di rileggere tutte le informazioni, quello storiche come 
#               name, tokenID, data di mint, etc che non cambieranno mai sarebbe utile memorizzarle
#               su un database oppure per semplicità in un file json da rileggere con le funzioni json
#       esempio di dati: 
#           - data del mio acquisto
#           - prezzo del mio acquisto (ETH e USD)
#           - fees
#           - prezzo con il quale ho messo in vendita per un certo periodo di tempo il mio NFT
#               questo definisce che l'NFT è attualmente in vendita
# 
#           - se l'NFT è stato Venduto allora si deve prendere in considerazione
#               - data di vendita
#               - prezzo di vendita definitivo
# #
# 
#   4) capire se è possibile leggere "solo" i nuovi dati , come ad esempio , le nuove offerte, senza 
#      impegnare le chiamate alle Opensea API. 
#       Insomma stabilire il metodo più efficiente. 
# 
#       esempio dati per singolo NFT:
#           - data dell'offerta più ALTA
#           - prezzo dell'offerta più ALTA
#           - data dell'offerta più BASSA (se utile visualizzarla)
#           - prezzo dell'offerta più BASSA
# 
#   5) costruire un layout con streamlit in forma di tabella #


