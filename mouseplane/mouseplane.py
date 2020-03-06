import gym
from math import sin, cos, radians, pi, atan2, degrees, sqrt
from enum import IntEnum
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
import pyautogui as ag

class MousePlaneEnv(gym.Env):
    
    def __init__(self, agent_pos, goal_pos, goal_size, width, height):
        assert width >= 3
        assert height >= 3

        self.width = width
        self.height = height
        self.agent_pos = agent_pos
        self.goal_pos = goal_pos
        self.goal_size = goal_size

        self.grid = [None] * width * height
        
    def reset(self):
        # Current position and direction of the agent
        self.init_pos = ag.position()
        self.agent_pos = self.init_pos
        self.goal_pos, self.goal_size = self.detectBox()
        self.init_dir = self.posToAngle(self.agent_pos, self.goal_pos)
        self.agent_dir = self.init_dir
        
        # These fields should have benn defined by the start of the episode
        assert self.agent_pos is not None
        assert self.goal_pos is not None

        # Step count since episode start
        self.step_count = 0

        # Return first observation
        obs = self.gen_obs()
        return obs
    
    def step(self, angle, distance, speed):
        self.step_count += 1
        reward = 0
        done = False
    
        # Calculate the position to move to
        self.agent_pos = np.add(self.agent_pos, self.angleToPos(self.agent_pos, angle, distance))
        ag.moveTo(self.agent_pos[0], self.agent_pos[1])
        
        # Calculate the new direction
        self.agent_dir = self.posToAngle(self.agent_pos, self.goal_pos)
     
        # Generate new observation/state
        obs = self.gen_obs()
        
        if self.agent_pos == self.goal_pos:
            ag.click()
            done = True
        
        if self.step_count >= self.max_steps:
            done = True
    
        return obs, reward, done, {}
    
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
        
    def gen_obs(self):
        obs = [*self.init_pos,
               *self.agent_pos,
               *self.goal_pos,
               *self.init_dir,
               *self.agent_dir,
               *self.goal_size]
        return obs
    
    def detectBox():
        """
        Returns:
          Bounding box of the goal in coordinates
    
        """
        # a, b =  viscapture
        return [500, 500], 10
    
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
        
class Plane:
    """
    Represent a screen plane and 
    """
    
    # Static cache of pre-renderer tiles
    tile_cache = {}

    def __init__(self, width, height):
        assert width >= 3
        assert height >= 3

        self.width = width
        self.height = height

        self.grid = [None] * width * height

    def __contains__(self, key):
        pass

    def __eq__(self, other):
        grid1  = self.encode()
        grid2 = other.encode()
        return np.array_equal(grid2, grid1)

    def __ne__(self, other):
        return not self == other

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def set(self, i, j, v):
        assert i >= 0 and i < self.width
        assert j >= 0 and j < self.height
        self.grid[j * self.width + i] = v

    def get(self, i, j):
        assert i >= 0 and i < self.width
        assert j >= 0 and j < self.height
        return self.grid[j * self.width + i]
    
    def get_grid(self):
        return self.plane


    def slice(self, topX, topY, width, height):
        """
        Get a subset of the plane
        """
        pass

    def render(
        self,
        tile_size,
        agent_pos=None,
        agent_dir=None,
        highlight_mask=None
    ):
        """
        Render this grid at a given scale
        :param r: target renderer object
        :param tile_size: tile size in pixels
        """
        pass

    def encode(self, vis_mask=None):
        """
        Produce a compact numpy encoding of the grid
        """
        pass

class MousePlaneEnv(gym.Env):
    """
    2D plane environment
    """

    # Enumeration of possible actions
    class Actions(IntEnum):
        # 
        angle = 0
        distance = 1
        speed = 2

    def __init__(
        self,
        plane_size=None,
        width=None,
        height=None,
        max_steps=1000,        
        seed=1337
    ):

        # Action enumeration for this environment
        self.actions = PlaneGridEnv.Actions

        # Actions are discrete integer values
        self.action_space = spaces.Discrete(len(self.actions))

        # Number of cells (width and height) in the agent view
        self.agent_view_size = agent_view_size

        # Observations are dictionaries containing an
        # encoding of the grid and a textual 'mission' string
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(self.agent_view_size, self.agent_view_size, 3),
            dtype='uint8'
        )
        self.observation_space = spaces.Dict({
            'image': self.observation_space
        })

        # Range of possible rewards
        self.reward_range = (0, 1)

        # Window to use for human rendering mode
        self.window = None

        # Environment configuration
        self.width = width
        self.height = height
        # self.low = low
        # self.high = high
        self.max_steps = max_steps
        self.see_through_walls = see_through_walls
        self.carrying = None

        # Current position of the agent
        self.agent_pos = None
        self.agent_dir = None
        
        # Position of the goal
        self.goal_pos = None

        # Initialize the RNG
        self.seed(seed=seed)

        # Initialize the state
        self.reset()

    def reset(self):
        # Current position and direction of the agent
        self.agent_pos = None
        self.agent_dir = None

        # To keep the same grid for each episode, call env.seed() with
        # the same seed before calling env.reset()
        self._gen_grid(self.width, self.height)
        
        # These fields should be defined by _gen_grid
        assert self.agent_pos is not None
        assert self.agent_dir is not None

        # print('%d , %d' % (self.width, self.height))

        # Check that the agent doesn't overlap with an object
        start_cell = self.grid.get(*self.agent_pos)
        assert start_cell is None or start_cell.can_overlap()

        # Step count since episode start
        self.step_count = 0

        # Return first observation
        obs = self.gen_obs()
        return obs

    def seed(self, seed=1337):
        # Seed the random number generator
        self.np_random, _ = seeding.np_random(seed)
        return [seed]

    @property
    def steps_remaining(self):
        return self.max_steps - self.step_count

    def reward(self):
        """
        Compute the reward to be given upon success
        """

        return 1 - 0.9 * (self.step_count / self.max_steps)

    def _rand_pos(self, xLow, xHigh, yLow, yHigh):
        """
        Generate a random (x,y) position tuple
        """

        return (
            self.np_random.randint(xLow, xHigh),
            self.np_random.randint(yLow, yHigh)
        )

    @property
    def dir_vec(self):
        """
        Get the direction vector for the agent, pointing in the direction
        of forward movement.
        """

        assert self.agent_dir >= 0 and self.agent_dir < 4
        return DIR_TO_VEC[self.agent_dir]

    @property
    def right_vec(self):
        """
        Get the vector pointing to the right of the agent.
        """

        dx, dy = self.dir_vec
        return np.array((-dy, dx))

    @property
    def front_pos(self):
        """
        Get the position of the cell that is right in front of the agent
        """

        return self.agent_pos + self.dir_vec

    def relative_coords(self, x, y):
        """
        Check if a grid position belongs to the agent's field of view, and returns the corresponding coordinates
        """

        vx, vy = self.get_view_coords(x, y)

        if vx < 0 or vy < 0 or vx >= self.agent_view_size or vy >= self.agent_view_size:
            return None

        return vx, vy

    def step(self, action):
        self.step_count += 1

        reward = 0
        done = False

        # Get the position in front of the agent
        fwd_pos = self.front_pos

        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)

        # Move right                
        if action == self.actions.right:
            self.agent_dir = 0
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos
            if fwd_cell != None and fwd_cell.type == 'goal':
                done = True
                reward = self._reward()
        
        # Move down
        elif action == self.actions.down:
            self.agent_dir = 1
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos
            if fwd_cell != None and fwd_cell.type == 'goal':
                done = True
                reward = self._reward()

        # Move left
        elif action == self.actions.left:
            self.agent_dir = 2
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos
            if fwd_cell != None and fwd_cell.type == 'goal':
                done = True
                reward = self._reward()
            
            
        # Move up
        elif action == self.actions.up:
            self.agent_dir = 3
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos
            if fwd_cell != None and fwd_cell.type == 'goal':
                done = True
                reward = self._reward()

        else:
            assert False, "unknown action"

        if self.step_count >= self.max_steps:
            done = True

        obs = self.gen_obs()

        return obs, reward, done, {}


    def render(self, mode='human', close=False, highlight=True, tile_size=TILE_PIXELS):
        """
        Render the whole-grid human view
        """
        pass
