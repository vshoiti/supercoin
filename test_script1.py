from Node import Node
import threading
import time


# ordem: coinServer, test_script1
# resultado esperado: os dois nós possuem o mesmo conjunto de peers, que contém os dois.


a = Node('1', 10026)
t_a = threading.Thread(target=a.start_node, kwargs={})
t_a.start()

time.sleep(3)
b = Node('2', 10027)
t_b = threading.Thread(target=b.start_node, kwargs={})
t_b.start()

time.sleep(3)

print(a.peers)
print(b.peers)
