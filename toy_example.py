from itertools import product, permutations
from util.input_to_DAG import toy_DAG
from util.task_scheduling import task_scheduler
import numpy as np

# Display
toy_DAG.display()


num_computers = 2
num_task = 4 + 1
mapping_dict =  {77: 0, 11: 1, 21: 2, 31 : 3, 41 : 4}  # task_id to chromosome location for computer_id

# Enumerate over all possible solution (chromosome)
'''
Each possible solution is represented as chromosome.
    Chormorsome is a List :
    [computer index for task_1 to task_5][task index in process order, need to follow condition of DAG]
    <--------- mapping------------------> <----------------------   scheduling ----------------------> 
    
    
    task_1 to task_5 is set as following:
        77,11,21,31,41
'''
enumerate_solution_list = []
computer_mapping_part = [([0] + list(combination)) for combination in product(range(num_computers), repeat=num_task - 1)]
tasks = [11, 21, 31, 41]
task_permutations_part = list(permutations(tasks))

# combine computer_mapping_part and task_permutations_part to form the complete chromosomes
optimal_time = np.inf
for mapping_part in computer_mapping_part:
    for scheduling_part in task_permutations_part:
        
        chromosome_list = list(mapping_part) + [77] + list(scheduling_part)
        #print(chromosome_list)
        my_task_scheduler = task_scheduler(chromosome_list, toy_DAG, num_task, num_computers, mapping_dict)
        _, _, _, _, check_feasible, time, fitness = my_task_scheduler.caculate_fitness()

        if check_feasible == True:
            if time < optimal_time:
                optimal_time = time
                optimal_solution = chromosome_list

print(f"\nOpitmal Time Found After Complete Enumeration : {optimal_time}")
print(f"\nThe best solution is (in term of chromosome): {optimal_solution}\n")

task_scheduler_ = task_scheduler(optimal_solution, toy_DAG, num_task, num_computers, mapping_dict)
task_scheduler_.caculate_fitness()
task_scheduler_.get_Gantt_chart_element()
task_scheduler_.plot_save_Gantt_chart('./figure/toy_eample/toy_best')