"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the AlgorithmManyArms class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)
"""

import numpy as np

# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE

class AlgorithmManyArms:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon=horizon
        self.t=0
        self.prevarm=0
        self.prevreward=0;
        self.values=np.zeros(num_arms)
        self.counts=np.zeros(num_arms)
        self.consecutive_m=np.zeros(num_arms)
        self.permute=np.random.permutation(num_arms)
        self.breakflag=False
        # Horizon is same as number of arms
    
    def give_pull(self):
        # START EDITING HERE
        
        
        m=np.int64(np.sqrt(self.horizon))
        
        if(len(self.permute)>0 and self.breakflag==False):
            if(self.consecutive_m[self.permute[0]]<m and self.consecutive_m[self.permute[0]]>=0):
                return self.permute[0]
            elif self.consecutive_m[self.permute[0]]==m:
                self.breakflag=True;
                return self.permute[0]
            else :
                self.permute=np.delete(self.permute,0)
                return self.permute[0]

        else:
            if len(self.permute)>0 :
                return self.permute[0]
            else :
                np.argmax(self.values)             

        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward==0 :
            self.consecutive_m[arm_index]=-1
        else :
            self.consecutive_m[arm_index]+=1

        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

        # END EDITING HERE
