from Node import Node
import threading
import time


# ordem: coinServer, test_script0
# resultado esperado: o nó se conecta e recebe uma lista vazia de peers.


a = Node('1', 10026)
t_a = threading.Thread(target=a.start_node, kwargs={})
t_a.start()
t_a.join()
