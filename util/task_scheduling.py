import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import numpy as np
import math


class task_scheduler:
    def __init__(self, chromosome, my_DAG, num_task,  num_computers, mapping_dict):
        self.chromosome = chromosome
        self.my_DAG = my_DAG
        self.num_task = num_task
        self.num_computers = num_computers

        self.CRO = {}

        self.feasible = True
        self.fitness = 0
        self.time = 1000
        self.Start_Time = [0]*num_task       
        self.End_Time = [0]*num_task  
        self.Set_up_record = []
        self.Transfer_record = []

        self.main_dict = {}
        self.set_up_dict = {}
        self.transfer_dict = {}

        self.mapping_dict = mapping_dict 

    def transfer_chromosome_to_CRO(self):
        '''
        CRO stands for "Computer Run Order", it's a dict:
        CRO = {0 : [41,21,13], 
            1 : [.....],
            ....
                }
        '''
        for i in range(self.num_computers):
            self.CRO[i] = []
        for task_order in range(self.num_task):
            task_id = self.chromosome[self.num_task + task_order]
            computer_id = self.chromosome[self.mapping_dict[task_id]]
            self.CRO[computer_id].append(task_id)

        return self.CRO


    def caculate_fitness(self):
        '''
        Chormorsome is a List :
        [computer index for task_1 to task_13][task index in process order, need to follow condition of DAG]
        <--------- mapping(13) ------------->  <--------------------  scheduling(13) ----------------------> 

        task_1 to task_13 is set as following:
            77,11,12,13,21,22,23,31,32,33,34,41,42
        
        
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
        chromosome = self.chromosome
        my_DAG = self.my_DAG
        num_task = self.num_task
        num_computers = self.num_computers
        mapping_dict = self.mapping_dict
        
        Start_Time = self.Start_Time      # recorde the time the procssing step of a task start
        End_Time = self.End_Time        # recorde the time the procssing step of a task end
        Ready_Time = [0]*num_computers  # for every computer, dynamically recorde the time when the computer is ready for new task
        Set_up_record = self.Set_up_record                # record set up activity as tuples (task_id, computer_id, start_time, end_time)
        Transfer_record = self.Transfer_record              # record transfer activity as tuples (task_id, source_computer_id, target_computer_id, start_time, end_time)

        for task_order in range(num_task):
            #print("check in for loop")
            if task_order == 0:
                # deal with the origin (77)
                #print("task_id : 77")
                #print(f"computer_id : {computer_id}")
                #print("parent_task_id : None")
                #print("parent_computer_id : None\n")
                continue

            # get the task_id、computer_id of the current task
            task_id = chromosome[num_task + task_order]
            computer_id = chromosome[mapping_dict[task_id]]
            
            # get the task_id、computer_id of the parent task
            parent_task_id = my_DAG.get_parent_nodes(task_id)[0]
            parent_computer_id = chromosome[mapping_dict[parent_task_id]]
            
            
            #print(f"task_id : {task_id}")
            #print(f"computer_id : {computer_id}")
            #print(f"parent_task_id : {parent_task_id}")
            #print(f"parent_computer_id : {parent_computer_id}")
                
            if parent_task_id == 77:
                    set_up_time = my_DAG.setup_costs[(parent_task_id, task_id)][computer_id]

                    set_up = (task_id, computer_id, Ready_Time[computer_id], Ready_Time[computer_id] + set_up_time)
                    Set_up_record.append(set_up)
                
                    Start_Time[mapping_dict[task_id]] = Ready_Time[computer_id] + set_up_time
                    End_Time[mapping_dict[task_id]] = Start_Time[mapping_dict[task_id]] + my_DAG.node_weights[task_id][computer_id]
                    Ready_Time[computer_id] = End_Time[mapping_dict[task_id]]
            
            elif (parent_computer_id == computer_id) and (Ready_Time[computer_id] == End_Time[mapping_dict[parent_task_id]]):
                ## Meaning parent and child tasks are run on the same computer continuously ##
                Start_Time[mapping_dict[task_id]] = Ready_Time[computer_id]
                End_Time[mapping_dict[task_id]] = Start_Time[mapping_dict[task_id]] + my_DAG.node_weights[task_id][computer_id]
                Ready_Time[computer_id] = End_Time[mapping_dict[task_id]]

            elif(parent_computer_id == computer_id) and (Ready_Time[computer_id] != End_Time[mapping_dict[parent_task_id]]):
                ## Maybe parent and child tasks run on same computer, but they were interuptted by task of other jobs ##
                ## Then, setup time for child task is needed ##
                set_up_time = my_DAG.setup_costs[(parent_task_id, task_id)][computer_id]

                set_up = (task_id, computer_id, Ready_Time[computer_id], Ready_Time[computer_id] + set_up_time)
                Set_up_record.append(set_up)
                
                Start_Time[mapping_dict[task_id]] = Ready_Time[computer_id] + set_up_time
                End_Time[mapping_dict[task_id]] = Start_Time[mapping_dict[task_id]] + my_DAG.node_weights[task_id][computer_id]
                Ready_Time[computer_id] = End_Time[mapping_dict[task_id]]

            elif(parent_computer_id != computer_id):
                ## Or maybe parent and child tasks were just run on different computers ##
                ## Then, delay(transfer) time and set up time is needed ##
                '''
                假設電腦1 TRANSFER TO 電腦2 :
                    電腦1 一定要在前一個task完成後馬上傳出
                    電腦1 可以在TRANSFER期間做任何事

                    電腦2 一定要在TRANSFER完成後剛好也完成setup，接下來馬上做Process
                    電腦2 也可以在TRANSFER期間做任何事
                '''
                Parent_end_time = End_Time[mapping_dict[parent_task_id]]
                set_up_time = my_DAG.setup_costs[(parent_task_id, task_id)][computer_id]
                transfer_time = my_DAG.delay_cost_matrix[parent_computer_id, computer_id]
        
                Data_arrival_time = Parent_end_time + transfer_time # 必須強制從這個時間點開始
                #Set_up_finsh_time = Ready_Time[computer_id] + set_up_time
                Start_Time[mapping_dict[task_id]] = Data_arrival_time

                # 看看有沒有違反 "setup 時間不夠，被computer_2中前面的task擠壓到了"
                # 或者是 "deliver時間不夠，被computer_2中前面的task擠壓到了" 
                if (Ready_Time[computer_id] > (Start_Time[mapping_dict[task_id]] - set_up_time)) or (Ready_Time[computer_id] > (Start_Time[mapping_dict[task_id]] - transfer_time)):
                    #print("Infeasible Chromosome")
                    self.feasible = False
                    self.time =  80 # A punishment on non-feasible solution --> fitness will be around 0.014
                    self.fitness = self.time_to_fitness()
                    # return empty dict and list
                    # 600 is penalty
                    return self.Start_Time, self.End_Time, self.Set_up_record, self.Transfer_record, self.feasible, self.time, self.fitness 
                                    
                else:
                    set_up = (task_id, computer_id,  Start_Time[mapping_dict[task_id]] - set_up_time, Start_Time[mapping_dict[task_id]])
                    Set_up_record.append(set_up)
                    transfer = (task_id, parent_computer_id, computer_id, Parent_end_time, Parent_end_time + transfer_time)
                    Transfer_record.append(transfer)
                    
                    End_Time[mapping_dict[task_id]] = Start_Time[mapping_dict[task_id]] + my_DAG.node_weights[task_id][computer_id]
                    Ready_Time[computer_id] = End_Time[mapping_dict[task_id]]
                
            else:
                print("logic error, you miss something !")

            #print(f"Ready Time : {Ready_Time}\n")

        #print("Feasible Chromosome")
        time = max(End_Time)
        self.feasible = True
        self.time = time
        self.fitness = self.time_to_fitness()
        self.Start_Time = Start_Time       
        self.End_Time = End_Time  
        self.Set_up_record = Set_up_record
        self.Transfer_record = Transfer_record

        return Start_Time, End_Time, Set_up_record, Transfer_record, self.feasible, self.time, self.fitness 

    def time_to_fitness(self):
        min_time = 15 # just a hyperparameter
        max_time = 35 # just a hyperparameter

        normalized_time = (self.time - min_time) / (max_time - min_time)
        fitness = 1.0 / (math.exp(normalized_time))
        return fitness

        

    def get_Gantt_chart_element(self):
        '''
        Calculate two dict, 
            Dict 1 : each key is computer_id, each element is a list representing what the computer is doing in each time frame !
            Dict 2 : recording any transfering activity in each time frame !
        '''

        if self.feasible == True:
            main_dict = self.main_dict
            set_up_dict = self.set_up_dict
            for i in range(self.num_computers):
                main_dict[i] = np.zeros(self.time) # element of the array stands for "第x秒末"
                set_up_dict[i] = np.zeros(self.time)
            
            # add set up activity
            for set_up in self.Set_up_record:
                task_id = set_up[0]
                computer_index = set_up[1]
                start = set_up[2]
                end = set_up[3]
                set_up_dict[computer_index][start:end] = task_id
            set_up_dict = {key: value.astype(int).tolist() for key, value in set_up_dict.items()}
            self.set_up_dict = set_up_dict

            # add main process activity
            for task_order in range(self.num_task):
                task_id = self.chromosome[self.num_task + task_order]
                computer_index = self.chromosome[self.mapping_dict[task_id]]
                main_dict[computer_index][self.Start_Time[self.mapping_dict[task_id]] : self.End_Time[self.mapping_dict[task_id]]] = task_id
            main_dict = {key: value.astype(int).tolist() for key, value in main_dict.items()}
            self.main_dict = main_dict

            # add transfer activity
            transfer_dict = self.transfer_dict 
            for i in range(self.num_computers):
                for j in range(self.num_computers):
                    if i != j:
                        transfer_dict[(i,j)] = np.zeros(self.time) 
                        transfer_dict[(j,i)] = np.zeros(self.time) # element of the array stands for "第x秒末"
            for transfer in self.Transfer_record:
                task_id = transfer[0]
                source_computer_index = transfer[1]
                target_computer_index = transfer[2]
                start = transfer[3]
                end = transfer[4]
                transfer_dict[(source_computer_index, target_computer_index)][start:end] = task_id
            transfer_dict = {key: value.astype(int).tolist() for key, value in transfer_dict.items()}
            self.transfer_dict = transfer_dict

            return main_dict, set_up_dict, transfer_dict

        else: 
            raise ValueError("只能對Feasible Solution 使用 get_Gantt_chart_element")
    
    def plot_save_Gantt_chart(self, save_file_name = None):
        '''
        For creating the Gantt Chart
        Quite Messy, suggest not to read in detail
        '''
        if self.feasible == True:
            data_1 = self.main_dict
            for key in data_1:
                data_1[key].extend([0] * 10)
            data_2 = self.set_up_dict
            data_3 = self.transfer_dict
            # Color Mapping
            colors = list(mcolors.TABLEAU_COLORS.keys())
            color_map = {task_id: colors[int(str(task_id)[0]) % len(colors)] if task_id != 0 else 'white' for task_id in set(x for lst in data_1.values() for x in lst)}
            light_skin_color = mcolors.to_rgba('peachpuff', 0.6)

            fig, ax = plt.subplots(figsize=(15, 10))  

            # Plot data_1
            for computer_id, tasks in data_1.items():
                start_time = 0
                for i in range(1, len(tasks)):
                    if tasks[i] != tasks[i-1]:
                        ax.broken_barh([(start_time, i-start_time)], (computer_id-0.4, 0.8), facecolors=color_map[tasks[i-1]])
                        if tasks[i-1] != 0:
                            ax.text(start_time, computer_id, str(tasks[i-1]), va='center', ha='left', color='black')
                        start_time = i
                ax.broken_barh([(start_time, len(tasks)-start_time)], (computer_id-0.4, 0.8), facecolors=color_map[tasks[-1]])

            # Plot data_2
            for computer_id, tasks in data_2.items():
                start_time = 0
                for i in range(1, len(tasks)):
                    if tasks[i] != tasks[i-1]:
                        ax.broken_barh([(start_time, i-start_time)], (computer_id-0.4, 0.8), facecolors=light_skin_color if tasks[i-1] != 0 else 'white', alpha=0.5)
                        if tasks[i-1] != 0:
                            ax.text(start_time, computer_id, str(tasks[i-1]), va='center', ha='left', color='black', alpha=0.5)
                        start_time = i
                ax.broken_barh([(start_time, len(tasks)-start_time)], (computer_id-0.4, 0.8), facecolors=light_skin_color if tasks[-1] != 0 else 'white', alpha=0.5)

            # Plot data_3
            for (comp1, comp2), tasks in data_3.items():
                for i, task in enumerate(tasks):
                    if task != 0:
                        # Black Line, 右上-->Upload；左下-->Download
                        ax.plot([i, i+1], [comp1 , comp1 + 0.2], color='black')
                        ax.plot([i, i+1], [comp2+0.2 , comp2], color='black')

            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Computer ID')
            ax.set_yticks(range(len(data_1)))
            ax.set_yticklabels(['Computer {}'.format(i+1) for i in range(len(data_1))])
            ax.set_title('Gantt Chart of Tasks on Computers')

            unique_jobs = set(int(str(task_id)[0]) for task_id in color_map if task_id != 0)
            legend_elements = [Patch(facecolor=colors[job % len(colors)], label='Job {}'.format(job)) for job in unique_jobs]
            legend_elements.append(Patch(facecolor=light_skin_color, label='Set Up'))
            ax.legend(handles=legend_elements)

            # Show the "Time"
            textstr = f"time: {self.time}"
            props = dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
            ax.text(0.97, 0.05, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='bottom', horizontalalignment='right', bbox=props)

            # Save the Plot
            if save_file_name is not None:
                plt.savefig(f'./{save_file_name}.png')
            # plt.show()
        else:
            raise ValueError("只能對Feasible Solution 使用 plot_save_Gantt_chart")