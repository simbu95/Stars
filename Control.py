from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy
import time

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

#need to set these to what the actual map size is
_Xsize=80
_Ysize=80
numpy.set_printoptions(threshold=numpy.inf)

class SimpleAgent(base_agent.BaseAgent):
    def __init__(self):
      self.G_State=State()
    def step(self, obs):
        super(SimpleAgent, self).step(obs)
        time.sleep(.05)
        if _MOVE_SCREEN in obs.observation["available_actions"]:
          self.G_State.Update(obs)
          return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, self.G_State.States(obs)])
        else:
          return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


class State(object):  #Need to add in state of player unit
  def __init__(self):
    self.squares=numpy.zeros((4,_Xsize,_Ysize))
  
  def States(self,obs):
    player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
    neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
    for p in zip(neutral_x, neutral_y):
      self.squares[2]=numpy.copy(self.squares[0])
      self.squares[3]=numpy.zeros((_Xsize,_Ysize))
      self.squares[2,p[0],p[1]]=0
      self.squares[3,p[0],p[1]]=1
      #Pick Best State
      #Q-Eval (self.squares)
      #if new best, save Best and evaluated value. 
    #Return Best State
    Best=[neutral_x[0], neutral_y[0]]
    return Best
  def Update(self,obs):
    self.squares=numpy.zeros((4,_Xsize,_Ysize))
    player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
    neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
    for p in zip(neutral_x, neutral_y):
      self.squares[0,p[0],p[1]]=1
    player_y, player_x = (player_relative == _PLAYER_FRIENDLY).nonzero()
    player = [int(player_x.mean()), int(player_y.mean())]
    self.squares[1,player[0],player[1]]=1


# Defining the state is hard  ... Mostly done
#but the task is easy
# keep a list of all minerals  ... Done
# move a marine to a mineral and remove the mineral ... Not Started
# one state for every mineral a marine can move to 
#with two marines, 2xminerals number of states. 