from Node import Node
import _thread
import time

a = Node('1', 10026)
_thread.start_new_thread(a.start_node, ())

time.sleep(3)
b = Node('2', 10027)
_thread.start_new_thread(b.start_node, ())

time.sleep(3)
print(a.peers)
print(b.peers)

a.start_miner()

time.sleep(3)

print('t')
b.send_transactions('1', 3)

time.sleep(10)