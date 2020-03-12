import gym
from math import sin, cos, radians, pi, atan2, degrees, sqrt
from enum import IntEnum
import numpy as np
import random
from gym import error, spaces, utils
from gym.utils import seeding
import pyautogui as ag
from gym.envs.registration import register

# Global environment definitions

FPS = 50

class MousePlaneEnv(gym.Env):
    
    def __init__(self, agent_pos, goal_pos, goal_size, width, height):
        assert width >= 3
        assert height >= 3

        self.width = width
        self.height = height
        self.agent_pos = agent_pos
        self.goal_pos = goal_pos
        self.goal_size = goal_size
        self.action_space = spaces.Box(np.array([0,-1]), np.array([+1,+1]), dtype=np.float32)  # angle, distance

        self.grid = [None] * width * height
        
        self.observation_space = spaces.Box(
            np.array([-500,-500,0,0,10,0]),
            np.array([500,500,360,360,100,100]),
            dtype='uint8')
        self.observation_space = spaces.Dict({
            'grid': self.observation_space
        })
        
        # does the embedding normalize? check if it is required here
        
    def reset(self):
        # Current position and direction of the agent
        self.init_pos = ag.position()
        self.agent_pos = self.init_pos
        self.goal_pos, self.goal_size = self.detectBox()
        self.init_dir = self.posToAngle(self.agent_pos, self.goal_pos)
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
        distance = action[0]*self.dist
        angle = (action[1]*45 + self.agent.dir) % 360
        
        # Move to new position
        self.agent_pos = np.add(self.agent_pos, self.angleToPos(self.agent_pos, distance, angle))
        ag.moveTo(self.agent_pos[0], self.agent_pos[1])
        
        # Calculate the new direction and speed
        self.agent_dir = self.posToAngle(self.agent_pos, self.goal_pos)
        self.speed = distance
        
        # Reward based on number of actions taken
        self.reward -= 0.01
        step_reward = self.reward -self.prev_reward
        self.prev_reward = self.reward
     
        # Generate new observation/state
        obs = self.gen_obs()
        
        if self.agent_pos == self.goal_pos:
            ag.click()
            self.reward += 1
            done = True
        
        if self.step_count >= self.max_steps:
            done = True
    
        return obs, step_reward, done, {}
    
    def posToDist(self, p0, p1):
        dx = (p0[0]-p1[0])**2
        dy = (p0[1]-p1[1])**2
        return sqrt(dx + dy)
    
    def posToAngle(self, p0, p1):
        angle = degrees(atan2(p1[1] - p0[1], p1[0] - p0[0]))
        return angle % 360
            
    def angleToPos(self, p0, distance, angle):
        theta = radians(angle)
        point = [int(p0[0] + distance * cos(theta)), int(p0[1] + distance * sin(theta))]
        return point
        
    # TO-DO: Consider relative mouse and goal positions
    # def gen_obs(self):
    #     obs = [*self.init_pos,
    #            *self.agent_pos,
    #            *self.goal_pos,
    #            *self.init_dir,
    #            *self.agent_dir,
    #            *self.goal_size,
    #            self.distance]
    #     return obs
    
    # Consider normalization 0-1
    def gen_obs(self):
        init = self.goal_pos - self.init_pos
        curr = self.goal_pos - self.agent_pos
        obs = [*init,
               *curr,
               *self.init_dir,
               *self.agent_dir,
               *self.goal_size,
               self.distance]
        return obs
    
    def detectBox():
        """
        Returns:
          Bounding box of the goal in coordinates
    
        """
        # a, b =  viscapture
        # random goal box
        return [random.randrange(500, 700), random.randrange(500, 700)], 10
    
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
    
register(
    id='MousePlane-v0',
    entry_point='mouseplane.envs:MousePlaneEnv'
)    