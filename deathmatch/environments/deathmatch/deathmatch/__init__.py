from gym.envs.registration import register

register(
    id='Deathmatch-v0',
    entry_point='deathmatch.envs:DeathmatchEnv',
)


