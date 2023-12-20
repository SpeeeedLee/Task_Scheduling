'''
Need to have
1. def Generate_next_generation():
    One_point_crossover / Order_crossover
    Mutation

2. def One_point_crossover():

3. def Order_crossover():

4. def Mutation():

5. def Tournament_selection

6. def Roulette_wheel_selection


'''

import random
import numpy as np 
from util.task_scheduling import task_scheduler

class GA_operator():

    def __init__(self, num_computers, num_task, population_size, total_round, my_DAG, mutation_prob):
        self.num_computers = num_computers
        self.num_task = num_task
        self.my_DAG = my_DAG
        self.population_size = population_size
        self.total_round = total_round
        self.mutation_prob = mutation_prob
        self.initial_generation = []
        self.current_generation = []
        

    def ramdom_initial_generation(self):
        '''
        Generate Random First Initial Generation

        Solution is expressed as chormosome(list):
        [computer index for task_1 to task_13][task index in process order, need to follow condition of DAG]
        <--------- mapping(13) ------------->  <--------------------  scheduling(13) ---------------------->
        '''
        initial_generation = []
        for _ in range(self.population_size):
            mapping_part = [random.randint(0, self.num_computers - 1) for _ in range(self.num_task)]
            scheduling_part = self.my_DAG.random_topological_sort()
            chromosome_list = mapping_part + scheduling_part
            initial_generation.append(chromosome_list)
        return initial_generation
    

    def feasible_initial_generation(self):
        '''
        Generate Only Feasible Solution for First Gereration
        '''
        initial_generation = []
        while len(initial_generation) < self.population_size:
            mapping_part = [random.randint(0, self.num_computers - 1) for _ in range(self.num_task)]
            scheduling_part = self.my_DAG.random_topological_sort()
            chromosome_list = mapping_part + scheduling_part
            my_task_scheduler = task_scheduler(chromosome_list, self.my_DAG, self.num_task,  self.num_computers)
            _, _, _, _, check_feasible, _, _ = my_task_scheduler.caculate_fitness()
            if check_feasible == True:
                initial_generation.append(chromosome_list)
        return initial_generation
    

    def mutation(self, chrom):
        '''
        Each position in the first part of the chromosome is subjected to mutation with a probability. 
        Which means change task from one computer to another.
        For each computer, 
            1. choose whether or not change the computer
            2. choose which computer to change to if selected in 1.
        '''
        mutated_chrom = chrom.copy()
        for task_order in range(self.num_task):
            random_num = random.random()
            if random_num < self.mutation_prob:
                original_computer_id = mutated_chrom[task_order]
                choices = [computer_id for computer_id in range(0, 5) if computer_id != original_computer_id]
                change_computer_id = random.choice(choices)
                mutated_chrom[task_order] = change_computer_id

        return mutated_chrom

    def one_point_cross_over(self, chrom_1, chrom_2):
        # remember there is one psuedo task "77"
        chrom_1_left = chrom_1[:self.num_task]
        chrom_2_left = chrom_2[:self.num_task]
        chrom_1_right = chrom_1[self.num_task :]
        chrom_2_right = chrom_2[self.num_task :]

        cross_over_point = random.randint(2, self.num_task - 1) # 2 到 12 的整數，表示child_1 想要左邊幾個

        chrom_child_1 = chrom_1_left[:cross_over_point] + chrom_2_left[cross_over_point:] + chrom_1_right
        chrom_child_2 = chrom_2_left[:cross_over_point] + chrom_1_left[cross_over_point:] + chrom_2_right

        return chrom_child_1, chrom_child_2
    

    def order_cross_over(self, chrom_1, chrom_2):
        # remember there is one psuedo task "77"

        cross_over_point_1 = random.randint(15, 2 * self.num_task - 2) # 15 到 24 的整數，表示 chrom_child_1 想留chrom左邊數來多少個數
        inherit_order = chrom_1[self.num_task : cross_over_point_1]
        remaining_order = [task for task in chrom_2[self.num_task : 2*self.num_task] if task not in inherit_order]
        chrom_child_1 = chrom_1[:self.num_task] + inherit_order + remaining_order 

        cross_over_point_2 = random.randint(15, 2 * self.num_task - 2) # 15 到 24 的整數，表示 chrom_child_1 想留chrom左邊數來多少個數
        inherit_order_2 = chrom_2[self.num_task : cross_over_point_2]
        remaining_order_2 = [task for task in chrom_1[self.num_task : 2*self.num_task] if task not in inherit_order_2]
        chrom_child_2 = chrom_2[:self.num_task] + inherit_order_2 + remaining_order_2 

        return chrom_child_1, chrom_child_2
    
    def Genetic_Algorithm_loop(self):
        self.initial_generation = self.feasible_initial_generation()
        self.current_generation = self.initial_generation
        
        shortest_time_found_list = []     # recording overall shoertest time so far
        shortest_time_in_rounds_list = [] # recording shortest round found in current round 
        best_solution_found_list = []     # recording the solution of overall shortest time found so far 

        # record the first generation
        print(f"\nFirst Generation !")
        chrom_list = []
        feasible_list = []
        time_list = []
        fitness_list = []
        shortest_time_in_round = np.inf
        for chrom in self.current_generation:
                scheduler = task_scheduler(chrom, self.my_DAG, self.num_task, self.num_computers)
                _, _, _, _, feasible, time, fitness = scheduler.caculate_fitness()
                if time < shortest_time_in_round:
                    shortest_time_in_round = time
                    best_solution_found_in_round = chrom
                chrom_list.append(chrom)
                feasible_list.append(feasible)
                time_list.append(time)
                fitness_list.append(fitness)
        shortest_time_in_rounds_list.append(shortest_time_in_round)
        shortest_time_found_list.append(shortest_time_in_round)
        best_solution_found_list.append(best_solution_found_in_round)
        print(f"Feasible : {feasible_list}")
        print(f"Time : {time_list}")
        print(f"Fitness : {fitness_list}")

        for round in range(self.total_round):
            print(f"\nStart {round + 1}-th GA !") 
            new_generation = []   
            append_feasible_fail = 0
            while len(new_generation) < self.population_size :
                # Roulette_wheel_selection to choose two parents                   
                parent_chorm_1, parent_chorm_2 = self.Roulette_wheel_selection(fitness_list)
            
                # Use these two parents to perform crossover
                '''40% do the order crossover, 40% do the one point crossover, 20% do the both'''
                random_crossover = random.uniform(0, 1)
                if random_crossover < 0.4:
                    chrom_child_1, chrom_child_2 = self.order_cross_over(parent_chorm_1, parent_chorm_2)
                    
                elif 0.4 <= random_crossover <= 0.8:
                    chrom_child_1, chrom_child_2 = self.one_point_cross_over(parent_chorm_1, parent_chorm_2)
                else:
                    chrom_child_1, chrom_child_2 = self.order_cross_over(parent_chorm_1, parent_chorm_2)
                    chrom_child_1, chrom_child_2 = self.one_point_cross_over(chrom_child_1, chrom_child_2)

                # Mutation on the produced two children           
                chrom_child_1_mutated = self.mutation(chrom_child_1)
                chrom_child_2_mutated = self.mutation(chrom_child_2)

                # check whether the two child is feasible
                scheduler_for_child_1 = task_scheduler(chrom_child_1_mutated, self.my_DAG, self.num_task, self.num_computers)
                _, _, _, _, feasible_child_1, _, _ = scheduler_for_child_1.caculate_fitness()
                
                scheduler_for_child_2 = task_scheduler(chrom_child_2_mutated, self.my_DAG, self.num_task, self.num_computers)
                _, _, _, _, feasible_child_2, _, _ = scheduler_for_child_2.caculate_fitness()

                # Append the feasible mutated children to the next generation 
                # However, allow to append non-feasible is try many time (maybe some non-feasible solution is with good DNA)
                # This can also prvent the while loop to take too much time !
                if feasible_child_1:
                    new_generation.append(chrom_child_1_mutated)
                else:
                    if append_feasible_fail <= 3*self.population_size:
                        append_feasible_fail += 1
                    else:
                        new_generation.append(chrom_child_1_mutated)         
                if feasible_child_2:
                    new_generation.append(chrom_child_2_mutated)
                else:
                    if append_feasible_fail <= 3*self.population_size:
                        append_feasible_fail += 1
                    else:
                        new_generation.append(chrom_child_2_mutated)  
            self.current_generation = new_generation
            
            # record the new generation
            chrom_list = []
            feasible_list = []
            time_list = []
            fitness_list = []
            shortest_time_in_round = np.inf
            for chrom in self.current_generation:
                    scheduler = task_scheduler(chrom, self.my_DAG, self.num_task, self.num_computers)
                    _, _, _, _, feasible, time, fitness = scheduler.caculate_fitness()
                    #chrom_list.append(chrom)
                    if time < shortest_time_in_round:
                        shortest_time_in_round = time
                        best_solution_found_in_round = chrom
                    feasible_list.append(feasible)
                    time_list.append(time)
                    fitness_list.append(fitness)
            shortest_time_in_rounds_list.append(shortest_time_in_round)
            if shortest_time_in_round < shortest_time_found_list[-1]:
                shortest_time_found_list.append(shortest_time_in_round)
                best_solution_found_list.append(best_solution_found_in_round)
            else:
                shortest_time_found_list.append(shortest_time_found_list[-1])
                best_solution_found_list.append(best_solution_found_list[-1])
            print(f"Feasible : {feasible_list}")
            print(f"Time : {time_list}")
            print(f"Fitness : {fitness_list}")

        return shortest_time_in_rounds_list, shortest_time_found_list, best_solution_found_list

    def Roulette_wheel_selection(self, fitness_list):
        '''
        select two parents out from self.current_generation

        Given self.current_generation, 
            1. calulate fitness each solution gets, and stored in S.
            2. calculate the probability of selection based on S, and stored in Prob, 
            3. get the selection results by roulette wheel selection.
        '''
        total_fitness = sum(fitness_list)

        selection_probs = [fitness / total_fitness for fitness in fitness_list]

        # choose two parents out
        parent_chrom_1 = self.current_generation[self.select_parent(selection_probs)]
        parent_chrom_2 = self.current_generation[self.select_parent(selection_probs)]

        return parent_chrom_1, parent_chrom_2

    def select_parent(self, selection_probs):
        '''Select two parents'''
        random_selection = random.uniform(0, 1)
        cumulative_probability = 0.0
        for index, prob in enumerate(selection_probs):
            cumulative_probability += prob
            if random_selection <= cumulative_probability:
                return index


