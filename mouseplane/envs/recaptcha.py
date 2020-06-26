import gym
from math import sin, cos, radians, pi, atan2, degrees, sqrt
from enum import IntEnum
import numpy as np
from random import randrange, choice, uniform
from gym import error, spaces, utils
from gym.utils import seeding
import pyautogui as ag
from gym.envs.registration import register
import requests
import time

# Global environment definitions

FPS = 50
ag.PAUSE = 0.01

class reCaptchaEnv(gym.Env):
    
    def __init__(self, agent_pos=None, goal_pos=None, goal_size=None, init_score=0.1, max_steps=50, step_size = 20):

        self.agent_pos = agent_pos
        self.goal_pos = goal_pos
        self.goal_size = goal_size
        self.action_space = spaces.Box(np.array([0,-1]), np.array([+1,+1]), dtype=np.float32)  # angle, distance
        self.max_steps = max_steps
        self.step_size = step_size
        self.init_score = init_score
        self.last_score = 0
        self.trajectory_dir = -1
        self.scores = []
        
        self.observation_space = spaces.Box(
            np.array([-500,-500,-500,-500,0]),
            np.array([500,500,500,500,1000]),
            dtype='uint8')
        self.observation_space = spaces.Dict({
            'image': self.observation_space
        })
        # obs = [initx, inity, currx, curry, idx, idy, adx, ady, self.goal_size, int(self.dist)]
        # does the embedding normalize? check if it is required here
        
    def reset(self):
        # Set direction and simulate human delay
        self.trajectory_dir *= -1
        time.sleep(uniform(0.5, 3))
        # Current position and direction of the agent
        self.init_pos = ag.position()
        self.agent_pos = self.init_pos
        self.goal_pos, self.goal_size = self.getGoal()
        self.init_dir = self.posToAngle(self.goal_pos, self.agent_pos)
        self.agent_dir = self.init_dir
        self.dist = self.posToDist(self.agent_pos, self.goal_pos)
        self.speed = 0
        
        self.reward = 0.0
        self.prev_reward = 0.0
        self.t = 0.0
        
        # These fields should have benn defined by the start of the episode
        assert self.agent_pos is not None
        assert self.goal_pos is not None

        # Step count since episode start
        self.step_count = 0

        # Return first observation
        obs = self.gen_obs()
        return obs
    
    def step(self, action):
        self.step_count += 1
        self.t += 1.0/FPS
        done = False
        
        # Convert to relative angle and distance
        distance = action[0]*self.dist/self.step_size
        angle = (action[1]*25*self.trajectory_dir + self.agent_dir) % 360
        
        # Move to new position
        self.agent_pos = self.angleToPos(self.agent_pos, distance, angle)
        # print([self.agent_pos[0], self.agent_pos[1]])
        ag.moveTo(self.agent_pos[0], self.agent_pos[1])
        
        # Calculate the new direction and speed
        self.agent_dir = self.posToAngle(self.agent_pos, self.goal_pos)
        self.speed = distance
     
        # Generate new observation/state
        obs = self.gen_obs()
        
        if self.goalBox():
            if self.trajectory_dir == 1:
                time.sleep(uniform(0.2, 0.5))
                ag.mouseDown()
                time.sleep(uniform(0.08, 0.12))
                ag.mouseUp()   
                r = requests.get("http://localhost:5000/alterego/result")
                result = r.json()["score"]
                self.scores.append(result)
                self.last_score = result
                self.reward += (result - self.last_score)
            else:
                self.reward += (self.last_score - self.init_score)
            # print('GOAL')
            done = True
        # if self.step_count >= self.max_steps:
        #     done = True
            
        # Add pentalty on steps taken
        self.reward -= 0.01
        step_reward = self.reward - self.prev_reward
        self.prev_reward = self.reward
    
        return obs, step_reward, done, {}
    
    def posToDist(self, p0, p1):
        dx = (p0[0]-p1[0])**2
        dy = (p0[1]-p1[1])**2
        return sqrt(dx + dy)
    
    def posToAngle(self, p0, p1):
        angle = degrees(atan2(p1[1] - p0[1], p1[0] - p0[0]))
        return angle % 360
            
    def angleToPos(self, p0, distance, angle):
        theta = radians(int(angle))
        point = [int(p0[0] + distance * cos(theta)), int(p0[1] + distance * sin(theta))]
        return point
        
    def goalBox(self):
        a = self.agent_pos[0] >= self.goal_pos[0]-self.goal_size and self.agent_pos[0] <= self.goal_pos[0]+self.goal_size
        b = self.agent_pos[1] >= self.goal_pos[1]-self.goal_size and self.agent_pos[1] <= self.goal_pos[1]+self.goal_size
        return a and b
        
    
    # Consider normalization 0-1
    def gen_obs(self):
        initx = self.goal_pos[0] - self.init_pos[0]
        inity = self.goal_pos[1] - self.init_pos[1]
        currx = self.goal_pos[0] - self.agent_pos[0]
        curry = self.goal_pos[1] - self.agent_pos[1]
        ind = self.init_dir
        agd = self.agent_dir
        # obs = np.array([initx, inity, currx, curry, ind, agd, self.goal_size, int(self.dist)])
        obs = np.array([initx, inity, currx, curry, int(self.dist)])
        return obs
    
    def getGoal(self):
        """
        Returns:
          Bounding box of the goal in coordinates, alternating between
          the trigger button and a random location near the border
    
        """
        if self.trajectory_dir == 1:
            goal = [490, 510]
        else:
            a = choice([(0,300),(700,1000)])
            b = choice([(200,400),(600,800)])
            goal = [randrange(*a), randrange(*b)]
        return goal, 8
    
    def getScores(self):
        return(self.scores)
    
    def articulatedTrajectory(x, y):
        """
        Executes the whole articulated mouse movement.
        
        Args:
        x : (int, None)
        y : (int, None)
        
        Returns
        None.
        """
        # Pre-train the model on a simulated environment to smoothen the movement
        
        # Yield trajectory parameters from the controller network
        # angle = 
        # speed = 
        # x = 
        # y = 
        # moveTo()
        pass


# for env in gym.envs.registry.env_specs:
#     if 'MousePlane-v0' not in env:
#         register(
#             id='MousePlane-v0',
#             entry_point='mouseplane.envs:MousePlaneEnv',
#             reward_threshold=0.95
#             )