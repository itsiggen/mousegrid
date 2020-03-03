from gym_minigrid.mousegrid import *
from gym_minigrid.register import register

class MiniGridMouse(MouseGridEnv):
    """
    Empty grid environment, no obstacles, sparse reward
    """

    def __init__(
        self,
        agent_start_pos=(1,1),
        agent_start_dir=0,
        width=None,
        height=None
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        super().__init__(
            width=width,
            height=height,
            max_steps=4*(width+height),
            agent_view_size=20,
            # Set this to True for maximum speed
            see_through_walls=True
        )

    def _gen_grid(self, width, height):
        # Create an empty grid of size NxM
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal square in the center
        self.put_obj(Goal(), width //2, height // 2)
        self.goal_pos = (width //2, height // 2)

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "i am a human"

class EmptyMouse(MiniGridMouse):
    def __init__(self):
        super().__init__(width=20, height=20, agent_start_pos=None)

register(
    id='MiniGrid-Mouse-v0',
    entry_point='gym_minigrid.envs:EmptyMouse'
)