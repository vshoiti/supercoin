from Node import Node
import threading
import time

# ordem: coinServer, test_script2, test_script3
# resultado esperado: recebe o bloco '...9b1d', transação aceita, pois o endereço 3 tem fundos


a = Node('3', 10028)
t_a = threading.Thread(target=a.start_node, kwargs={})
t_a.start()

time.sleep(3)
print(a.peers)

time.sleep(3)

print('###### t ######')
a.send_transactions('1', 3)

t_a.join()

