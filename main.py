'''
This is where one want to run the code

1. Create a Task Table, Delay Matrix
2. Generate DAG (from Task Table, Delay Matrix)
3. Generate random initial population that statisfy topology structue of DAG
4. Evaluation(using DAG)  --> Tournament Selection/ Roulette Wheel Selection
5. Crossover & Mutation
6. Back to step 4.
'''



'''
For every Computer, we will have below dict:
    RT --> Ready Time of the computer 
        example : {1: 10, 2:3, ....}


For all tasks, we will have below Dict:
    ST --> Start Time for different tasks
        {(i, j) = starting time, ......}
        ex:
        {(1,1) = 2, (1,2,1) = 6....}
    FT --> Start Time for different tasks
        {(i, j) = finish time, ......}
        ex:
        {(1,1) = 2, (1,2,1) = 6....}


'''
import numpy as np 
from util.task_scheduling import task_scheduler
from util.GA import GA_operator
from util.input_2_DAG import my_DAG, num_computers, num_task

# Generate random initail generation
population_size = 10
total_round = 3000
my_GA_operator = GA_operator(num_computers, num_task, population_size, total_round, my_DAG, 0.25)

#shortest_time_in_rounds_list, shortest_time_found_list, best_solution_found_list = my_GA_operator.Genetic_Algorithm_loop()


#print(shortest_time_found_list[-1])
#print(best_solution_found_list[-1])

chrom = [2, 0, 2, 2, 1, 1, 0, 3, 3, 3, 3, 2, 4, 77, 21, 31, 41, 22, 42, 11, 12, 13, 32, 33, 34, 23]
task_schedule_1 = task_scheduler(chrom, my_DAG, num_task,  num_computers)
task_schedule_1.caculate_fitness()
task_schedule_1.get_Gantt_chart_element()
task_schedule_1.plot_save_Gantt_chart('./figure/time_18')
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