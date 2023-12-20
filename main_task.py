import numpy as np 
from util.task_scheduling import task_scheduler
from util.GA import GA_operator
from util.SA import SA_operator
from util.input_to_DAG import my_DAG


# Display
my_DAG.display()

num_computers = 5
num_task = 12 + 1

mapping_dict =  {77: 0,
                        11: 1, 12: 2, 13: 3,
                        21: 4, 22: 5, 23: 6,
                        31: 7, 32: 8, 33: 9, 34: 10,
                        41: 11, 42: 12}  # task_id to chromosome location for computer_id

'''<============================================= Genetic Algorithm =================================================>'''
'''
# Setting some Hyperparemeters
population_size = 10
total_round = 3000
mutation_prob = 0.2

# Instantiate the GA operator
my_GA_operator = GA_operator(num_computers, num_task, population_size, total_round, my_DAG, mutation_prob, mapping_dict)

GA_shortest_time_in_rounds_list, GA_shortest_time_found_list, GA_best_solution_found_list = my_GA_operator.Genetic_Algorithm_loop()

# Save the best result found !
GA_best_solution_found = GA_best_solution_found_list[-1]
print(f"Best Solution Found : {GA_best_solution_found}")
task_schedule_1 = task_scheduler(GA_best_solution_found, my_DAG, num_task,  num_computers, mapping_dict)
task_schedule_1.caculate_fitness()
task_schedule_1.get_Gantt_chart_element()
task_schedule_1.plot_save_Gantt_chart('./figure/main_task/GA.png')

'''


'''<============================================= Simulated Annealing =================================================>'''
# Setting some Hyperparemeters
total_round = 30000
mutation_prob = 0.2
mutate_order_portion = 0.08
start_Temp = 0.7


# Instantiate the SA operator
my_SA_operator = SA_operator(num_computers, num_task, total_round, my_DAG, mutation_prob, mapping_dict, mutate_order_portion, start_Temp)
SA_shortest_time_found_list, SA_best_solution_found_list= my_SA_operator.Simulated_Annealing_loop()

# Save the best result found !
SA_best_solution_found = SA_best_solution_found_list[-1]
print(f"Best Solution Found : {SA_best_solution_found}")
task_schedule_1 = task_scheduler(SA_best_solution_found, my_DAG, num_task,  num_computers, mapping_dict)
task_schedule_1.caculate_fitness()
task_schedule_1.get_Gantt_chart_element()
task_schedule_1.plot_save_Gantt_chart('./figure/main_task/SA.png')



'''<========================================= Particle Swarm Optimization ============================================>'''









'''<=========================================  Plot the Progress Diagram  ============================================>'''

'''
feasible_initial_solution = my_GA_operator.feasible_initial_generation()
print(feasible_initial_solution)

x1 = feasible_initial_solution[0]
x2 = feasible_initial_solution[1]

child_1, child_2 = my_GA_operator.one_point_cross_over(x1, x2)
child_1_order, child_2_order = my_GA_operator.order_cross_over(x1, x2)
child_mutation = my_GA_operator.mutation(x1)


print("\n================ One Point Crossover ===============")
print (f"Parnet 1 : {x1}")
print (f"Parnet 2 : {x2}")
print (f"\nChild 1 : {child_1}")
print (f"Child 2 : {child_2}")

print("\n================ Order Crossover ===============")
print (f"Parnet 1 : {x1}")
print (f"Parnet 2 : {x2}")
print (f"\nChild 1 : {child_1_order}")
print (f"Child 2 : {child_2_order}")

print("\n================     Mutation     ===============")
print (f"Parnet : {x1}")
print (f"\nChild : {child_mutation}")


'''

'''
task_schedule_1 = task_scheduler(x1, my_DAG, num_task,  num_computers)
task_schedule_1.caculate_fitness()
task_schedule_1.get_Gantt_chart_element()
task_schedule_1.plot_save_Gantt_chart('./figure/feasible_3')
'''

'''
print(first_generation[0])
print(my_DAG.node_weights[77][0])
print(my_DAG.setup_costs[(22, 23)][3])
print(chromosome_to_CRO(first_generation[0], num_task, num_computers))
'''
'''
for chromosome in first_generation:
    task_schedule_1 = task_scheduling(chromosome, my_DAG, num_task,  num_computers)
    task_schedule_1.transfer_chromosome_to_CRO()
    task_schedule_1.caculate_fitness()
    if task_schedule_1.feasible:
        task_schedule_1.get_Gantt_chart_element()
        print(f"find a feasible : {chromosome}")
        # plot 
        
        print(f"\nStart Time : {task_schedule_1.Start_Time}")
        print(f"\nEnd Time : {task_schedule_1.End_Time}")
        print(f"\nSet Up Record : {task_schedule_1.Set_up_record}")
        print(f"\nTransfer Record : {task_schedule_1.Transfer_record}")
        print(f"\nFitness : {task_schedule_1.fitness}")
        print(f"\nCRO : {task_schedule_1.CRO}")
        print(f"\nMain Dict : {task_schedule_1.main_dict}")
        print(f"\nSet Up Dict : {task_schedule_1.set_up_dict}")
        print(f"\nTransfer Dict : {task_schedule_1.transfer_dict}")
        
    else:
        print("find not feasible")
'''

'''
chromosome =  [0, 0, 1, 1, 4, 4, 2, 2, 2, 2, 4, 0, 3, 77, 41, 42, 21, 22, 11, 12, 23, 13, 31, 32, 33, 34]
task_schedule_1 = task_scheduling(chromosome, my_DAG, num_task,  num_computers)
task_schedule_1.transfer_chromosome_to_CRO()
task_schedule_1.caculate_fitness()
task_schedule_1.get_Gantt_chart_element()
task_schedule_1.plot_save_Gantt_chart('first_generation')
print(f"\nMain Dict : {task_schedule_1.main_dict}")
print(f"\nSet Up Dict : {task_schedule_1.set_up_dict}")
print(f"\nTransfer Dict : {task_schedule_1.transfer_dict}")
'''