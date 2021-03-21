from Environments import *
from GameFeatures import GameFeatures as GF

class SetupFiles:
    def first_features():
        map_setup = { "X": {"Color": GF.BlockColor.Black, "Effect": GF.BlockEffect.Block}, 
              "O": {"Color": GF.BlockColor.White, "Effect": GF.BlockEffect.Nothing} }

        f1 = GF()
        f1.add_map_layout(GF.MapLayout.DefaultMap1, map_setup)
        f1.add_start_position((3, 3))
        f1.add_controls(GF.Controls.UpDown)
        f1.add_block(GF.BlockColor.Red, GF.BlockEffect.TakeLife, [(4, 5), (4, 10), (6, 7), (6, 8), (7, 5), (7, 10), (8, 6), (8, 7), (8, 8), (8, 9), (9, 3)], effect_strength=5)

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

        return [f1, f2, f3, f4]


    def project_features():
        SS1_map_setup = { "X": {"Color": GF.BlockColor.Black, "Effect": GF.BlockEffect.Block}, 
                          "O": {"Color": GF.BlockColor.White, "Effect": GF.BlockEffect.Nothing} }

        SS12_map_setup = { "X": {"Color": GF.BlockColor.Red, "Effect": GF.BlockEffect.Block}, 
                           "O": {"Color": GF.BlockColor.Blue, "Effect": GF.BlockEffect.Nothing} }

        SS13_map_setup = { "X": {"Color": GF.BlockColor.Blue, "Effect": GF.BlockEffect.Block}, 
                           "O": {"Color": GF.BlockColor.Red, "Effect": GF.BlockEffect.Nothing} }

        f1 = GF()
        f1.add_map_layout(GF.MapLayout.DefaultMap2, SS1_map_setup)
        f1.add_survival_property(GF.SurvivalProperty.Starve, interval=10, strength=1)
        f1.add_item(GF.ItemColor.Yellow, GF.ItemEffect.GivePoints, GF.ItemBehaviour.Respawn, [(3, 12), (5, 5), (7, 9), (10, 13)], 30, 1)
        f1.add_item(GF.ItemColor.Green, GF.ItemEffect.GiveLife, GF.ItemBehaviour.Respawn, [(2, 2), (4, 12), (11, 4), (13, 9)], 30, 1)
        f1.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.LeftRight, [(13, 8)], speed=1, effect_strength=1)
        f1.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Black, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.UpDown, [(12, 3)], speed=1, effect_strength=1)
        f1.add_start_position((3, 3))

        f2 = GF()
        f2.add_map_layout(GF.MapLayout.DefaultMap2, SS1_map_setup)
        f2.add_survival_property(GF.SurvivalProperty.Starve, interval=10, strength=1)
        f2.add_item(GF.ItemColor.Yellow, GF.ItemEffect.GivePoints, GF.ItemBehaviour.Respawn, [(3, 12), (5, 5), (7, 9), (10, 13)], 30, 1)
        f2.add_item(GF.ItemColor.Green, GF.ItemEffect.GiveLife, GF.ItemBehaviour.Respawn, [(2, 2), (4, 12), (11, 4), (13, 9)], 30, 1)
        f2.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.UpDown, [(12, 6)], speed=1, effect_strength=5)
        f2.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Black, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.LeftRight, [(7, 6)], speed=1, effect_strength=1)
        f2.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.LeftRight, [(13, 8)], speed=1, effect_strength=1)
        f2.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Black, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.UpDown, [(12, 3)], speed=1, effect_strength=1)
        f2.add_block(GF.BlockColor.Green, GF.BlockEffect.GiveLife, [(11, 8)], effect_strength=1)
        f2.add_start_position((3, 3))

        f3 = GF()
        f3.add_map_layout(GF.MapLayout.DefaultMap3, SS1_map_setup)
        f3.add_survival_property(GF.SurvivalProperty.Starve, interval=10, strength=1)
        f3.add_item(GF.ItemColor.Blue, GF.ItemEffect.GivePoints, GF.ItemBehaviour.Respawn, [(6, 2), (13, 2), (2, 13), (8, 13)], 40, 1)
        f3.add_item(GF.ItemColor.Green, GF.ItemEffect.GiveLife, GF.ItemBehaviour.Respawn, [(4, 6), (5, 7), (11, 7), (10, 9), (9, 2)], 40, 1)
        f3.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.UpDown, [(11, 13)], speed=1, effect_strength=1)
        f3.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.LeftRight, [(12, 10)], speed=1, effect_strength=1)
        f3.add_start_position((3, 3))

        f4 = GF()
        f4.add_map_layout(GF.MapLayout.DefaultMap3, SS1_map_setup)
        f4.add_survival_property(GF.SurvivalProperty.Starve, interval=10, strength=1)
        f4.add_item(GF.ItemColor.Blue, GF.ItemEffect.GivePoints, GF.ItemBehaviour.Respawn, [(6, 2), (13, 2), (2, 13), (8, 13)], 40, 1)
        f4.add_item(GF.ItemColor.Green, GF.ItemEffect.GiveLife, GF.ItemBehaviour.Respawn, [(4, 6), (5, 7), (11, 7), (10, 9), (9, 2)], 40, 1)
        f4.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Black, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.LeftRight, [(2, 9), (10, 10)], speed=1, effect_strength=1)
        f4.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Black, GF.MonsterEffect.TakeLife, GF.MonsterBehaviour.UpDown, [(11, 5)], speed=1, effect_strength=1)
        f4.add_block(GF.BlockColor.Red, GF.BlockEffect.TakeLife, [(3, 11), (9, 3), (12, 6), (13, 8), (13, 9)], effect_strength=1)
        f4.add_start_position((3, 3))

        f5 = GF()
        f5.add_map_layout(GF.MapLayout.DefaultMap1, SS12_map_setup)
        f5.add_item(GF.ItemColor.Blue, GF.ItemEffect.TakeLife, GF.ItemBehaviour.Respawn, [(9, 5), (6, 9), (8, 13), (11, 12), (13, 9)], 1, 5)
        f5.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Red, GF.MonsterEffect.GiveLife, GF.MonsterBehaviour.DiagonalRight, [(11, 5), (11, 11)], 2, 1)
        f5.add_block(GF.BlockColor.Green, GF.BlockEffect.TakeLife, [(5, 6), (3, 12), (12, 3), (9, 9)], 1)
        f5.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.White, GF.MonsterEffect.GivePoints, GF.MonsterBehaviour.DiagonalRight, [(11, 7), (4, 11)], 2, 1)
        f5.add_start_position((3, 4))

        f6 = GF()
        f6.add_map_layout(GF.MapLayout.DefaultMap4, SS13_map_setup)
        f6.add_start_position((4, 10))
        f6.add_item(GF.ItemColor.Yellow, GF.ItemEffect.TakeLife, GF.ItemBehaviour.Nothing, [(2, 5), (2, 9), (2, 10), (3, 6), (5, 6), (7, 5), (7, 8), (8, 10), (9, 5), (9, 12), (10, 7), (10, 12), (11, 12), (12, 9), (14, 8)], 1, 25)
        f6.add_monster(GF.MonsterType.Invincible, GF.MonsterColor.Black, GF.MonsterEffect.Nothing, GF.MonsterBehaviour.Nothing, [(6, 4), (6, 11), (7, 7), (8, 8), (9, 4)], 0, 0)
        f6.add_block(GF.BlockColor.Green, GF.BlockEffect.Nothing, [(3, 7), (3, 8), (12, 7), (12, 8), (7, 3), (8, 3), (7, 12), (8, 12)], 0)


        return [f2, f1, f2, f3, f4, f5, f6]
