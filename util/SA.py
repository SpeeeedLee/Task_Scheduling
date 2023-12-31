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
    
    def create_pseudo_parent(slef, chrom):
        jobs = {}
        for task in chrom[1:]:  
            job_id = task // 10
            if job_id not in jobs:
                jobs[job_id] = []
            jobs[job_id].append(task)

        for job_id in jobs:
            jobs[job_id].sort()

        job_ids = list(jobs.keys())
        random.shuffle(job_ids)
        pseudo_parent = [77]  
        for job_id in job_ids:
            pseudo_parent.extend(jobs[job_id])

        return pseudo_parent

    def mutation_order(self, chrom):
        '''
        Leave the left part unchanged, 
        Crossover the right part with a psuedo parent
        '''
        pseudo_parent = self.create_pseudo_parent(chrom[self.num_task:])
        pseudo_parent_chrom = [0]*self.num_task + pseudo_parent

        cross_over_point = random.randint(15, 2 * self.num_task - 2) # 15 到 24 的整數，表示 mutated_chrom 想留chrom左邊數來多少個數
        inherit_order = chrom[self.num_task : cross_over_point]
        remaining_order = [task for task in pseudo_parent_chrom[self.num_task : 2*self.num_task] if task not in inherit_order]
        mutated_chrom = chrom[:self.num_task] + inherit_order + remaining_order 
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
        curr_chrom, curr_time, curr_fitness = self.feasible_initial_chrom()
        best_chrom = curr_chrom
        best_time = curr_time
        best_fitness = curr_fitness
        best_chrom_list.append(best_chrom)
        best_time_list.append(best_time)
        best_fitness_list.append(best_fitness)

        for round in range(self.total_round):
            print(f"SA : Start the {round + 1} iteration")
            
            # Mutated !
            Found_feasible_nieghbor = False
            while(Found_feasible_nieghbor == False):
                random_number = random.random()
                '''(1-20%)*mutate_order_portion do mutate order, (1-20%)*(1-mutate_order_portion) do mutate computer, 20% do the both'''
                if random_number < 0.8*self.mutate_order_portion:
                    mutated_chrom = self.mutation_order(curr_chrom)
                elif 0.8*self.mutate_order_portion <= random_number < 0.8:
                    mutated_chrom = self.mutation_computer(curr_chrom)
                else:
                    mutated_chrom = self.mutation_order(curr_chrom)
                    mutated_chrom = self.mutation_computer(curr_chrom)

                # Check if feasible
                task_scheduler_ = task_scheduler(mutated_chrom, self.my_DAG, self.num_task,  self.num_computers, self.mapping_dict)
                _, _, _, _, check_feasible, mutated_time, mutated_fitness = task_scheduler_.caculate_fitness()

                if check_feasible == True:
                    Found_feasible_nieghbor = True
            
            # Check if the time of the mutated chrom is smaller than curr_chrom
            if mutated_fitness > curr_fitness:
                curr_chrom = mutated_chrom
                curr_time = mutated_time
                curr_fitness = mutated_fitness
                if mutated_fitness > best_fitness:
                    best_chrom = mutated_chrom
                    best_time = mutated_time
                    best_fitness = mutated_fitness
            else:
                # accept the worse chromosome with probability
                dealta_E = curr_fitness - mutated_fitness
                curr_Temp = self.get_Temp_Linear(round)
                random_number = random.random()
                if (np.exp(-(dealta_E) / curr_Temp) > random_number):
                    curr_chrom = mutated_chrom
                    curr_time = mutated_time
                    curr_fitness = mutated_fitness
            best_chrom_list.append(best_chrom)
            best_time_list.append(best_time)
            best_fitness_list.append(best_fitness)
        
        return  best_time_list, best_chrom_list