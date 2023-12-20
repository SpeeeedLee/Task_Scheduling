import numpy as np 
from util.DAG import DAG

'''Creat a Direct Acyclic Graph instance for Problem 1'''
Delay_cost_matrix = np.array([[0,1], 
                              [2,0]])


Task_process_matrix_1 = np.array([[3,3]])
Task_process_matrix_2 = np.array([[5,5]])
Task_process_matrix_3 = np.array([[9,9]])
Task_process_matrix_4 = np.array([[8,8]])

Task_set_up_matrix_1 = np.array([[1,1]])
Task_set_up_matrix_2 = np.array([[1,1]])
Task_set_up_matrix_3 = np.array([[1,1]])
Task_set_up_matrix_4 = np.array([[1,1]])

toy_DAG = DAG(Delay_cost_matrix)

toy_DAG.add_node_task_cost(77, np.array([0,0]))
toy_DAG.add_node_task_cost(11, Task_process_matrix_1[0])
toy_DAG.add_node_task_cost(21, Task_process_matrix_2[0])
toy_DAG.add_node_task_cost(31, Task_process_matrix_3[0])
toy_DAG.add_node_task_cost(41, Task_process_matrix_4[0])

# Add set up cost 
# At the same time create the topological structure (a representation of the ordering among tasks) 
toy_DAG.add_setup_edge_cost(77, 11, Task_set_up_matrix_1[0])
toy_DAG.add_setup_edge_cost(77, 21, Task_set_up_matrix_2[0])
toy_DAG.add_setup_edge_cost(77, 31, Task_set_up_matrix_3[0])
toy_DAG.add_setup_edge_cost(77, 41, Task_set_up_matrix_4[0])






'''Create a Direct Acyclic Grpah instance for Problem 3'''
Delay_cost_matrix = np.array([[0,4,2,1,3],
                         [1,0,5,1,5],
                         [1,3,0,2,3],
                         [3,1,3,0,1],
                         [4,2,5,3,0]])

Task_process_matrix_1 = np.array([[2,5,4,1,2],
                                 [5,4,5,7,5],
                                 [4,5,5,4,5]])
Task_process_matrix_2 = np.array([[2,5,4,7,8],
                                 [5,6,9,8,5],
                                 [4,5,4,54,5]])
Task_process_matrix_3 = np.array([[9,8,6,7,9],
                                 [6,1,2,5,4],
                                 [2,5,4,2,4],
                                 [4,5,2,1,5]])
Task_process_matrix_4 = np.array([[1,5,2,4,12],
                                 [5,1,2,1,2]])

Task_set_up_matrix_1 = np.array([[1,3,1,1,2],
                                 [3,1,2,6,1],
                                 [1,4,4,2,2]])
Task_set_up_matrix_2 = np.array([[2,4,1,5,7],
                                 [1,6,7,4,3],
                                 [2,3,3,43,4]])
Task_set_up_matrix_3 = np.array([[4,7,4,3,9],
                                 [6,1,2,3,1],
                                 [1,5,1,1,2],
                                 [4,1,2,1,3]])
Task_set_up_matrix_4 = np.array([[1,1,1,8,8],
                                 [4,1,1,1,1]])


my_DAG = DAG(Delay_cost_matrix)


# Add task process cost
my_DAG.add_node_task_cost(77, np.array([0,0,0,0,0]))

my_DAG.add_node_task_cost(11, Task_process_matrix_1[0])
my_DAG.add_node_task_cost(12, Task_process_matrix_1[1])
my_DAG.add_node_task_cost(13, Task_process_matrix_1[2])

my_DAG.add_node_task_cost(21, Task_process_matrix_2[0])
my_DAG.add_node_task_cost(22, Task_process_matrix_2[0])
my_DAG.add_node_task_cost(23, Task_process_matrix_2[0])

my_DAG.add_node_task_cost(31, Task_process_matrix_3[0])
my_DAG.add_node_task_cost(32, Task_process_matrix_3[1])
my_DAG.add_node_task_cost(33, Task_process_matrix_3[2])
my_DAG.add_node_task_cost(34, Task_process_matrix_3[3])

my_DAG.add_node_task_cost(41, Task_process_matrix_4[0])
my_DAG.add_node_task_cost(42, Task_process_matrix_4[1])


# Add set up cost 
# At the same time create the topological structure (a representation of the ordering among tasks) 
my_DAG.add_setup_edge_cost(77, 11, Task_set_up_matrix_1[0])
my_DAG.add_setup_edge_cost(11, 12, Task_set_up_matrix_1[1])
my_DAG.add_setup_edge_cost(12, 13, Task_set_up_matrix_1[2])

my_DAG.add_setup_edge_cost(77, 21, Task_set_up_matrix_2[0])
my_DAG.add_setup_edge_cost(21, 22, Task_set_up_matrix_2[1])
my_DAG.add_setup_edge_cost(22, 23, Task_set_up_matrix_2[2])

my_DAG.add_setup_edge_cost(77, 31, Task_set_up_matrix_3[0])
my_DAG.add_setup_edge_cost(31, 32, Task_set_up_matrix_3[1])
my_DAG.add_setup_edge_cost(32, 33, Task_set_up_matrix_3[2])
my_DAG.add_setup_edge_cost(33, 34, Task_set_up_matrix_3[3])

my_DAG.add_setup_edge_cost(77, 41, Task_set_up_matrix_4[0])
my_DAG.add_setup_edge_cost(41, 42, Task_set_up_matrix_4[1])
