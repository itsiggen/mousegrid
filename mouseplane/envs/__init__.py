from mouseplane.envs.mouseplane import *
from mouseplane.envs.recaptcha import *
from gym.envs.registration import register

register(
        id='MousePlane-v0',
        entry_point='mouseplane.envs:MousePlaneEnv',
        reward_threshold=0.95
        )

register(
        id='reCaptcha-v0',
        entry_point='mouseplane.envs:reCaptchaEnv',
        reward_threshold=0.7
        )
