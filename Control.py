from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]
_SELECT_ALL = [0]

class SimpleAgent(base_agent.BaseAgent):
    def step(self, obs):
        super(SimpleAgent, self).step(obs)
        if _MOVE_SCREEN in obs.observation["available_actions"]:
          player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
          neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
          player_y, player_x = (player_relative == _PLAYER_FRIENDLY).nonzero()
          if not neutral_y.any() or not player_y.any():
            return actions.FunctionCall(_NO_OP, [])
          player = [int(player_x.mean()), int(player_y.mean())]
          closest, min_dist = None, None
          for p in zip(neutral_x, neutral_y):
            dist = numpy.linalg.norm(numpy.array(player) - numpy.array(p))
            if not min_dist or dist < min_dist:
              closest, min_dist = p, dist
          return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, closest])
        else:
          return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])