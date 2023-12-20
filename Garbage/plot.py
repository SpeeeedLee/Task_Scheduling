'''
Any kinds of function that is related to Plotting


'''
import numpy as np 

def Gantt_chart(Start_Time, End_Time, Set_up_record, Transfer_record, fitness, num_computers):
    '''
    Calculate two dict, 
        Dict 1 : each key is computer_id, each element is a list representing what the computer is doing in each time frame !
        Dict 2 : recording any transfering activity in each time frame !
    '''
    # Calculate Max First 


    main_dict = {}
    for i in range(num_computers):
        main_dict[i] = np.array
    
    # add set up activity
    for set_up in Set_up_record:
        computer_index = set_up[1]
        main_dict[computer_index] 

    


