from Environments import *
from BehaviouralModels import *
from GameFeatures import GameFeatures as GF


#----------- Generate Game Features -----------
map_setup = { "X": {"Color": GF.BlockColor.Black, "Effect": GF.BlockEffect.Block}, 
              "O": {"Color": GF.BlockColor.White, "Effect": GF.BlockEffect.Nothing} }

f1 = GF()
f1.add_map_layout(GF.MapLayout.DefaultMap1, map_setup)
f1.add_start_position((3, 3))
f1.add_controls(GF.Controls.UpDown)

f2 = GF()
f2.add_map_layout(GF.MapLayout.DefaultMap2, map_setup)
f2.add_start_position((3, 3))
f2.add_item(GF.ItemColor.Blue, GF.ItemEffect.GivePoints, GF.ItemBehaviour.Respawn, [(12, 5), (3, 6)], effect_strength=10, respawn_time=4)
f2.add_controls(GF.Controls.LeftRight)

f3 = GF()
f3.add_map_layout(GF.MapLayout.DefaultMap2, map_setup)
f3.add_start_position((3, 3))
f3.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.Kill, GF.MonsterBehaviour.LeftRight, [(7, 6)], speed=2)
f3.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.Kill, GF.MonsterBehaviour.UpDown, [(12, 9)])
f3.add_controls(GF.Controls.AllArrows)

f4 = GF()
f4.add_map_layout(GF.MapLayout.Empty14x14, map_setup)
f4.add_start_position((7, 7))
f4.add_controls(GF.Controls.AllArrows)
f4.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Blue, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.DiagonalLeft, [(8, 8)], effect_strength=10)
f4.add_survival_property(GF.SurvivalProperty.Starve, strength=2, interval=3)
f4.add_survival_property(GF.SurvivalProperty.Slowdown, strength=2)

#-------------------- Main --------------------
suite = EnvironmentSuit(4, BehaviouralModelInterface, features=[f1, f2, f3, f4], verbose = 2)
suite.run(512)

