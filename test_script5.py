from Node import Node
import threading
import time


# ordem: coinServer, test_script5
# resultado esperado: nó se conecta ao servidor na AWS e recebe uma lista de peers


Node.SERVER = '18.231.174.232'

a = Node('1', 63153)
t_a = threading.Thread(target=a.start_node, kwargs={})
t_a.start()
t_a.join()
