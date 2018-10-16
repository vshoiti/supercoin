from Node import Node
import threading
import time


# resultado esperado: 9 transações aceitas, resto rejeitada, bloco minerado e propagado


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
