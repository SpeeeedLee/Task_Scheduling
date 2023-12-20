import random
import numpy as np 
import itertools
from util.task_scheduling import task_scheduler


'''
"Tabu" in three ways:
1. Mutation Operation using Mutation_Order (Tabu Tenure = 10)
2. Psuedo Parent in Order Mutation (Tabu Tenure = 20) 

This means that if Mutation_Order is used, then ban it for 10 operations
And also, when the next time Mutation_Order is availabel and used, need to use completely different psudeo parents to cross over with
(All possible number of psuedo parents is 4! = 24, so we set the Tabu Tenure a little lower than 24)

3. Accept first mutation solution (i.e. no while loop to find feasible-solution only) (Tabu Tenure = 6)
   * Can not record that solution's time and fitness if it is not feasible
'''

class TS_operator():
    def __init__(self, num_computers, num_task, total_round, my_DAG, mutation_prob, mapping_dict, mutate_order_portion, Tenure_mutation_order, Tabu_Tenure_job_order):
        self.num_computers = num_computers
        self.num_task = num_task
        self.my_DAG = my_DAG
        self.mutation_prob = mutation_prob
        self.mutate_order_portion = mutate_order_portion
        self.total_round = total_round
        self.mapping_dict = mapping_dict
        self.Tenure_mutation_order = Tenure_mutation_order
        self.Mutaion_operator_used = False
        self.current_round = 0
        self.last_time_order_mutation = 0
        self.Tabu_job_order = []
        self.Tabu_Tenure_job_order = Tabu_Tenure_job_order
    
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


    def create_pseudo_parent_W_Tabu(self,chrom):
        
        if len(self.Tabu_job_order) > self.Tabu_Tenure_job_order:
            self.Tabu_job_order.pop()
        
        all_permutations = list(itertools.permutations(range(1, self.num_computers)))
        random.shuffle(all_permutations)

        for permutation in all_permutations:
            if permutation not in self.Tabu_job_order:
                job_ids = permutation
                break
        jobs = {}
        for task in chrom[1:]:  
            job_id = task // 10
            if job_id not in jobs:
                jobs[job_id] = []
            jobs[job_id].append(task)

        for job_id in jobs:
            jobs[job_id].sort()
        pseudo_parent = [77]  
        for job_id in job_ids:
            pseudo_parent.extend(jobs[job_id])

        self.Tabu_job_order.append(job_ids)
         
        return pseudo_parent

    def mutation_order(self, chrom):
        '''
        Leave the left part unchanged, 
        Crossover the right part with a psuedo parent
        '''
        pseudo_parent = self.create_pseudo_parent_W_Tabu(chrom[self.num_task:])
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

    def Tabu_mutaion_order(self, used = False):
        if used:
            self.last_time_order_mutation = self.current_round
        if self.last_time_order_mutation + self.Tenure_mutation_order < self.current_round:
            return True
        else:
            return False

    def Tabu_Search_loop(self):
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
            print(f"TS : Start the {round + 1} iteration")
            self.current_round += 1
            # Mutated !
            Found_feasible_nieghbor = False
            while(Found_feasible_nieghbor == False):
                Mutation_order_ban = self.Tabu_mutaion_order()
                if Mutation_order_ban == True:
                    # can only do mutaion_computer !
                    mutated_chrom = self.mutation_order(curr_chrom)
                else:
                    random_number = random.random()
                    '''(1-20%)*mutate_order_portion do mutate order, (1-20%)*(1-mutate_order_portion) do mutate computer, 20% do the both'''
                    if random_number < 0.8*self.mutate_order_portion:
                        mutated_chrom = self.mutation_order(curr_chrom)
                        self.Tabu_mutaion_order(True)
                    elif 0.8*self.mutate_order_portion <= random_number < 0.8:
                        mutated_chrom = self.mutation_computer(curr_chrom)
                    else:
                        mutated_chrom = self.mutation_order(curr_chrom)
                        mutated_chrom = self.mutation_computer(curr_chrom)
                        self.Tabu_mutaion_order(True)

                # Check if feasible
                task_scheduler_ = task_scheduler(mutated_chrom, self.my_DAG, self.num_task,  self.num_computers, self.mapping_dict)
                _, _, _, _, check_feasible, mutated_time, mutated_fitness = task_scheduler_.caculate_fitness()

                if check_feasible == True:
                    Found_feasible_nieghbor = True
            
            # Check if the time of the mutated chrom is smaller than best_chrom
            if mutated_fitness > best_fitness:
                best_chrom = mutated_chrom
                best_time = mutated_time
                best_fitness = mutated_fitness
                            
            best_chrom_list.append(best_chrom)
            best_time_list.append(best_time)
            best_fitness_list.append(best_fitness)
        
            # Starts from the mutated solution in the next round !
            curr_chrom = mutated_chrom
            curr_time = mutated_time
            curr_fitness = mutated_fitness

        return  best_time_list, best_chrom_list

