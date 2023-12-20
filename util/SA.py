import random
import numpy as np 
from util.task_scheduling import task_scheduler

class SA_operator():
    def __init__(self, num_computers, num_task, total_round, my_DAG, mutation_prob, mapping_dict, mutate_order_portion, start_Temp):
        self.num_computers = num_computers
        self.num_task = num_task
        self.my_DAG = my_DAG
        self.mutation_prob = mutation_prob
        self.mutate_order_portion = mutate_order_portion
        self.total_round = total_round
        self.mapping_dict = mapping_dict
        self.start_Temp = start_Temp

    def get_Temp_Linear(self, curr_round):
        '''
        To decide the hyperparameter start_Temp, one can reference on the following :
            exp(-1) = 0.368
        
        One can ask "how much (dealta E) in the first iteration do I want so that it will be accepted by prob = 0.368 ?"
        --> My ans for this is 0.7
        '''

        cuur_Temp = self.start_Temp * (1 - (curr_round /self.total_round))

        return cuur_Temp
    
    def feasible_initial_chrom(self):
        '''
        Generate A Feasible Solution for the First Round
        '''
        Found = False
        while Found == False:
            mapping_part = [random.randint(0, self.num_computers - 1) for _ in range(self.num_task)]
            scheduling_part = self.my_DAG.random_topological_sort()
            chromosome_list = mapping_part + scheduling_part
            my_task_scheduler = task_scheduler(chromosome_list, self.my_DAG, self.num_task,  self.num_computers, self.mapping_dict)
            _, _, _, _, check_feasible, time, fitness = my_task_scheduler.caculate_fitness()
            if check_feasible == True:
                return chromosome_list, time, fitness


    def mutation_order(self, chrom):
        '''
        Leave the left part unchanged, 
        Directly Pick another order from my_DAG for the rigth part
        '''
        mutated_scheduling_part = self.my_DAG.random_topological_sort()
        mutated_chrom = chrom[:self.num_task] + mutated_scheduling_part

        return mutated_chrom

    def mutation_computer(self, chrom):
        '''
        Leave the right part unchanged,
        Only mutate left part 
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



    def Simulated_Annealing_loop(self):
        # record every round
        best_chrom_list = []
        best_time_list = []
        best_fitness_list = []

        # Generate a random feasible solution for the first round
        best_chorm, best_time, best_fitness = self.feasible_initial_chrom()
        best_chrom_list.append(best_chorm)
        best_time_list.append(best_time)
        best_fitness_list.append(best_fitness)

        for round in range(self.total_round):
            print(f"SA : Start the {round + 1} iteration")
            
            # Mutated !
            Found_feasible_nieghbor = False
            while(Found_feasible_nieghbor == False):
                random_number = random.random()
                if random_number < self.mutate_order_portion:
                    mutated_chrom = self.mutation_order(best_chorm)
                else:
                    mutated_chrom = self.mutation_computer(best_chorm)

                # Check if feasible
                task_scheduler_ = task_scheduler(best_chorm, self.my_DAG, self.num_task,  self.num_computers, self.mapping_dict)
                _, _, _, _, check_feasible, time, fitness = task_scheduler_.caculate_fitness()

                if check_feasible == True:
                    Found_feasible_nieghbor = True  
            
            # Check if the time of the mutated chrom is smaller
            if fitness > best_fitness:
                best_chorm = mutated_chrom
                best_time = time
                best_fitness = fitness
                best_chrom_list.append(best_chorm)
                best_time_list.append(best_time)
                best_fitness_list.append(fitness)
            else:
                # accept the worse chromosome with probability
                dealta_E = best_fitness - fitness
                curr_Temp = self.get_Temp_Linear(round)
                random_number = random.random()
                if (np.exp(-(dealta_E) / curr_Temp) > random_number):
                    best_chrom_list.append(best_chorm)
                    best_time_list.append(best_time)
        
        return  best_time_list, best_chrom_list