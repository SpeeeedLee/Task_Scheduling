import numpy as np 
import matplotlib.pyplot as plt

from util.task_scheduling import task_scheduler
from util.GA import GA_operator
from util.SA import SA_operator
from util.TS import TS_operator
from util.input_to_DAG import my_DAG

def run(exp_num, population_size, FE_round):

    # Display the DAG
    my_DAG.display()
    num_computers = 5
    num_task = 12 + 1
    mapping_dict =  {77: 0,
                            11: 1, 12: 2, 13: 3,
                            21: 4, 22: 5, 23: 6,
                            31: 7, 32: 8, 33: 9, 34: 10,
                            41: 11, 42: 12}  # task_id to chromosome location for computer_id

    GA_best_time_found_list_exp = []
    SA_best_time_found_list_exp = []
    TS_best_time_found_list_exp = []


    for exp in range(exp_num):

        '''<============================================= Genetic Algorithm =================================================>'''
        # Setting some Hyperparemeters
        # population_size = 10
        total_round = FE_round // population_size
        mutation_prob = 0.2

        # Instantiate the GA operator
        my_GA_operator = GA_operator(num_computers, num_task, population_size, total_round, my_DAG, mutation_prob, mapping_dict)

        GA_shortest_time_in_rounds_list, GA_shortest_time_found_list, GA_best_solution_found_list = my_GA_operator.Genetic_Algorithm_loop()

        GA_best_time_found_list_exp.append(GA_shortest_time_found_list)

        # Save the best result found !
        GA_best_solution_found = GA_best_solution_found_list[-1]
        print(f"Best Solution Found : {GA_best_solution_found}")
        task_schedule_1 = task_scheduler(GA_best_solution_found, my_DAG, num_task,  num_computers, mapping_dict)
        task_schedule_1.caculate_fitness()
        task_schedule_1.get_Gantt_chart_element()
        task_schedule_1.plot_save_Gantt_chart(f'./figure/main_task/GA/GA_{exp}.png')



        '''<============================================= Simulated Annealing =================================================>'''
        # Setting some Hyperparemeters
        total_round = FE_round
        mutation_prob = 0.15
        mutate_order_portion = 0.2
        start_Temp = 0.7


        # Instantiate the SA operator
        my_SA_operator = SA_operator(num_computers, num_task, total_round, my_DAG, mutation_prob, mapping_dict, mutate_order_portion, start_Temp)
        SA_shortest_time_found_list, SA_best_solution_found_list= my_SA_operator.Simulated_Annealing_loop()

        SA_best_time_found_list_exp.append(SA_shortest_time_found_list)

        # Save the best result found !
        SA_best_solution_found = SA_best_solution_found_list[-1]
        print(f"Best Solution Found : {SA_best_solution_found}")
        task_schedule_1 = task_scheduler(SA_best_solution_found, my_DAG, num_task,  num_computers, mapping_dict)
        task_schedule_1.caculate_fitness()
        task_schedule_1.get_Gantt_chart_element()
        task_schedule_1.plot_save_Gantt_chart(f'./figure/main_task/SA/SA_{exp}.png')

        
        '''<============================================ Tabu Search =================================================>'''

        # Setting some Hyperparemeters
        total_round = FE_round
        mutation_prob = 0.15
        mutate_order_portion = 0.2 
        Tenure_mutation_order = 10
        Tabu_Tenure_job_order = 20

        # Instantiate the TS operator
        my_TS_operator = TS_operator(num_computers, num_task, total_round, my_DAG, mutation_prob, mapping_dict, mutate_order_portion, Tenure_mutation_order, Tabu_Tenure_job_order)
        TS_shortest_time_found_list, TS_best_solution_found_list= my_TS_operator.Tabu_Search_loop()

        TS_best_time_found_list_exp.append(TS_shortest_time_found_list)

        # Save the best result found !
        TS_best_solution_found = TS_best_solution_found_list[-1]
        print(f"Best Solution Found : {TS_best_solution_found}")
        task_schedule_1 = task_scheduler(TS_best_solution_found, my_DAG, num_task,  num_computers, mapping_dict)
        task_schedule_1.caculate_fitness()
        task_schedule_1.get_Gantt_chart_element()
        task_schedule_1.plot_save_Gantt_chart(f'./figure/main_task/TS/TS_{exp}.png')

    return GA_best_time_found_list_exp, SA_best_time_found_list_exp, TS_best_time_found_list_exp

'''<=========================================  Plot the Progress Diagram  ============================================>'''

def plot_progress_diagram(means1, stds1, means2, stds2, means3, stds3):
    '''
    Given the experiment data as input, plot and save the desired diagram
    '''

    plt.figure(figsize=(18, 12))  

    x_len = min(len(means1), len(means2))
    x_values = range(x_len)

    plt.plot(x_values, means1[:x_len], label='GA', marker='', linestyle='-')
    plt.plot(x_values, means2[:x_len], label='SA', marker='', linestyle='-')
    plt.plot(x_values, means3[:x_len], label='TS', marker='', linestyle='-')

    plt.fill_between(x_values, np.array(means1)[:x_len] - np.array(stds1)[:x_len], np.array(means1)[:x_len] + np.array(stds1)[:x_len], alpha=0.3)
    plt.fill_between(x_values, np.array(means2)[:x_len] - np.array(stds2)[:x_len], np.array(means2)[:x_len] + np.array(stds2)[:x_len], alpha=0.3)
    plt.fill_between(x_values, np.array(means3)[:x_len] - np.array(stds2)[:x_len], np.array(means3)[:x_len] + np.array(stds3)[:x_len], alpha=0.3)

    plt.xlabel('Function Evaluation Used')
    plt.ylabel('Min Process Time Found')
    plt.title('Comparison of 3 different algorithms')

    x_tick_positions = x_values[::5000]
    x_tick_labels = x_tick_positions  
    plt.xticks(x_tick_positions, x_tick_labels)
    
    plt.ylim(10, 80) 
    
    plt.legend()
    plt.grid(True)
    plt.savefig('./figure/main_task/progress_diagram.png')




if __name__ == '__main__':

    ##### Change these three parameters #####
    num_exp = 5
    population_size = 10
    FE_round = 8000
    ##########################################

    S_GA, S_SA, S_TS = run(num_exp, population_size, FE_round)

    S_GA_arr = np.array(S_GA)
    S_SA_arr = np.array(S_SA)
    S_TS_arr = np.array(S_TS)

    GA_means = np.mean(S_GA_arr, axis=0).tolist()
    SA_means = np.mean(S_SA_arr, axis=0).tolist()
    TS_means = np.mean(S_TS_arr, axis=0).tolist()
    
    GA_stds = np.std(S_GA_arr, axis=0).tolist()
    SA_stds = np.std(S_SA_arr, axis=0).tolist()
    TS_stds = np.std(S_TS_arr, axis=0).tolist()

    # Need to "strech" the results of GA"
    expanded_GA_means = [item for item in GA_means for _ in range(population_size)]
    expanded_GA_stds = [item for item in GA_stds for _ in range(population_size)]

    plot_progress_diagram(expanded_GA_means, expanded_GA_stds, SA_means, SA_stds, TS_means, TS_stds)