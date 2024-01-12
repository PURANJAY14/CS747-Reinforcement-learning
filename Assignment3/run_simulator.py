from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        # Replace with your implementation to determine actions to be taken
        action_steer = None
        action_acc = None

        action = np.array([action_steer, action_acc])  

        return action

    def align_state(self,state):

        act=[0,0];f=False
        if state[3]>180 :
            state[3]=state[3]-360

        angle=(180/3.14159)*np.arctan((state[1]-0)/(state[0]-350.0))
        #print(state[3],angle)
        if angle>180 :
            angle=angle-360

        if state[3]-angle<0:
            act=[2,0]

        if abs(state[3]-angle)<2.5:
            f=True

        return f,act


    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            f=False
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action=[1,4]
                if not f:
                    f,action=self.align_state(state)
                 
                #action = self.dict[self.choose_action(get_features(state),weights,epsilon)]
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                  
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        action_steer = None
        action_acc = None

        action = np.array([action_steer, action_acc])  

        return action

    def vertical_obstacle(self,state,ran_cen_list):
        for i in range(4):
            if ran_cen_list[i][1]*state[1]>0 and abs(state[1])>abs(ran_cen_list[i][1]):
                if abs(state[0]-ran_cen_list[i][0])<=65:
                    return True
        return False

    def horizontal_obstacle(self,state,ran_cen_list):
        for i in range(4):
            if ran_cen_list[i][1]*state[1]>0 and state[0]<0 and ran_cen_list[i][0]>0:
                if abs(state[1]-ran_cen_list[i][1])<=65:
                    return True
        return False

    def align_state(self,state,final_angle):

        act=[0,0];f=False
        if state[3]>180 :
            state[3]=state[3]-360

        angle=final_angle
        #print(state[3],angle)
        if angle>180 :
            angle=angle-360

        if state[3]-angle<0:
            act=[2,0]

        if abs(state[3]-angle)<2.0:
            #print(state[3]-angle,angle,state[3])
            f=True

        return f,act

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            road_status = False
            type_state=0
            first_step_done=False
            second_step_done=False
            third_step_done=False

            if not self.vertical_obstacle(state,ran_cen_list):
                type_state=1
            #print(type_state)
            if type_state==0:
                if self.horizontal_obstacle(state,ran_cen_list):
                    initial_angle=(180/3.14159)*np.sign(state[1])*np.arctan((315-state[1])/(315-state[0]))
                    #print(initial_angle,state,ran_cen_list)
                else:
                    initial_angle=0
            else :
                if state[1]<0:
                    initial_angle=90.0
                else:
                    initial_angle=-90.0                
            f=False
            while not f:
                f,action=self.align_state(state,initial_angle)
                if not f:
                    state, reward, terminate, reached_road, info_dict = simulator._step(action)
                    cur_time += 1


            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                if type_state==0:
                    if not second_step_done:
                        if state[0]>310 and state[0]<328:
                            second_step_done=True
                            action=[1,0]
                            state, reward, terminate, reached_road, info_dict = simulator._step(action)
                            state, reward, terminate, reached_road, info_dict = simulator._step(action)
                            cur_time += 2
                        else:
                            action=[1,4]
                            state, reward, terminate, reached_road, info_dict = simulator._step(action)
                            cur_time += 1
                    elif not third_step_done:
                        f=False
                        while not f:

                            f,action=self.align_state(state,(180/3.14159)*np.arctan((state[1]-0)/(state[0]-350.0)))
                            if not f:
                                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                                cur_time += 1
                        #print(state,(180/3.14159)*np.arctan((state[1]-0)/(state[0]-350.0)))
                        third_step_done=True

                    else:
                        action=[1,4]
                        state, reward, terminate, reached_road, info_dict = simulator._step(action)
                        cur_time += 1

                if type_state==1:
                    if not second_step_done:
                        if state[1]>- 7 and state[1]<7:
                                second_step_done=True
                                action=[1,0]
                                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                                #print(state)
                                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                                cur_time += 2
                        else:
                            action=[1,4]
                            state, reward, terminate, reached_road, info_dict = simulator._step(action)
                            cur_time += 1

                    elif not third_step_done:
                        f=False
                        while not f:
                            f,action=self.align_state(state,(180/3.14159)*np.arctan((state[1]-0)/(state[0]-350.0)))
                            state, reward, terminate, reached_road, info_dict = simulator._step(action)
                            cur_time += 1
                        third_step_done=True
                    else:
                        action=[1,4]
                        state, reward, terminate, reached_road, info_dict = simulator._step(action)
                        cur_time += 1


                # action = self.next_action(state)
                # state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                # cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
