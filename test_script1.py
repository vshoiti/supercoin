from Node import Node
import threading
import time

a = Node('1', 10026)
t_a = threading.Thread(target=a.start_node, kwargs={})
t_a.start()
t_a.join()
