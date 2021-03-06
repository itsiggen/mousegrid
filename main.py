from mouseplane.PPO import PPO, Memory
import gym
import torch
import numpy as np
import pyautogui as ag

############## Hyperparameters ##############
env_name = "reCaptcha-v0"
render = False
solved_reward = 0.5         # stop training if avg_reward > solved_reward
log_interval = 20           # print avg reward in the interval
max_episodes = 100          # max training episode
max_timesteps = 50          # max timesteps in one episode

update_timestep = 40        # update policy every n timesteps
action_std = 0.2            # constant std for action distribution (Multivariate Normal)
K_epochs = 80               # update policy for K epochs
eps_clip = 0.2              # clip parameter for PPO
gamma = 0.99                # discount factor

lr = 0.0003                 # parameters for Adam optimizer
betas = (0.9, 0.999)

random_seed = None
#############################################

# creating environment
env = gym.make(env_name, init_score=0.1)
state_dim = env.observation_space["image"].shape[0]
action_dim = env.action_space.shape[0]

if random_seed:
    print("Random Seed: {}".format(random_seed))
    torch.manual_seed(random_seed)
    env.seed(random_seed)
    np.random.seed(random_seed)

memory = Memory()
ppo = PPO(state_dim, action_dim, action_std, lr, betas, gamma, K_epochs, eps_clip)
print(lr,betas)

# logging variables
running_reward = 0
avg_length = 0
time_step = 0
scores = []

#move to initial point in screen
ag.moveTo(990, 260, duration=1, tween=ag.easeOutQuad)  
# training loop
for i_episode in range(1, max_episodes+1):
    state = env.reset()
    for t in range(max_timesteps):
        time_step +=1
        # Running policy_old:
        action = ppo.select_action(state, memory)
        state, reward, done, _ = env.step(action)
        
        # Saving reward and is_terminals:
        memory.rewards.append(reward)
        memory.is_terminals.append(done)
        
        # update if its time
        if time_step % update_timestep == 0:
            ppo.update(memory)
            memory.clear_memory()
            time_step = 0
        running_reward += reward
        if render:
            env.render()
        if done:
            break
    
    avg_length += t
    
    # stop training if avg_reward > solved_reward
    if running_reward > (log_interval*solved_reward):
        print("########## Solved! ##########")
        torch.save(ppo.policy.state_dict(), './PPO_continuous_solved_{}.pth'.format(env_name))
        break
    
    # save every 20 episodes
    if i_episode % 20 == 0:
        torch.save(ppo.policy.state_dict(), './PPO_continuous_{}.pth'.format(env_name))
        scores = env.getScores()
        
    # logging
    if i_episode % log_interval == 0:
        avg_length = int(avg_length/log_interval)
        running_reward = round(running_reward/log_interval, 2)
        
        print('Episode {} \t Avg length: {} \t Avg reward: {}'.format(i_episode, avg_length, running_reward))
        running_reward = 0
        avg_length = 0
        
