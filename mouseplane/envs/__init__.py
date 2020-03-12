from mouseplane import *
from gym.envs.registration import register

register(
    id='Mouseplane-v0',
    entry_point='mouseplane.envs:MousePlaneEnv'
)  
