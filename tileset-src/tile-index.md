# Tileset coordinate key

`[col, row]` on the 32x32 grid of `tileset-lexy.png` (pixel = col*32, row*32). `×N` = cells in that tile's animation / direction set. ✅ = already re-skinned.

## terrain

| tile | col,row | cells |
|---|---|---|
| `floor` ✅ | 0, 2 | 3 |
| `floor_letter` | 1, 2 | 1 |
| `hint` | 2, 2 | 1 |
| `wall_invisible` | 3, 2 | 2 |
| `popwall` | 4, 2 | 1 |
| `fake_floor` | 5, 2 | 2 |
| `popdown_floor` | 6, 2 | 2 |
| `canopy` | 7, 2 | 2 |
| `dirt` ✅ | 8, 2 | 1 |
| `sand` ✅ | 9, 2 | 1 |
| `grass` ✅ | 10, 2 | 1 |
| `hole` ✅ | 12, 2 | 2 |
| `cracked_floor` ✅ | 13, 2 | 1 |
| `wall` ✅ | 0, 3 | 1 |
| `steel` ✅ | 1, 3 | 3 |
| `wall_appearing` | 3, 3 | 1 |
| `popwall2` | 4, 3 | 1 |
| `fake_wall` | 5, 3 | 1 |
| `popdown_wall` | 6, 3 | 1 |
| `gravel` ✅ | 8, 3 | 1 |
| `spikes` ✅ | 9, 3 | 1 |
| `floor_custom_green` ✅ | 8, 4 | 1 |
| `floor_custom_pink` ✅ | 9, 4 | 1 |
| `floor_custom_yellow` ✅ | 10, 4 | 1 |
| `floor_custom_blue` ✅ | 11, 4 | 1 |
| `thin_walls` | 12, 4 | 2 |
| `one_way_walls` | 13, 4 | 2 |
| `wall_custom_green` ✅ | 8, 5 | 1 |
| `wall_custom_pink` ✅ | 9, 5 | 1 |
| `wall_custom_yellow` ✅ | 10, 5 | 1 |
| `wall_custom_blue` ✅ | 11, 5 | 1 |
| `turtle` | 4, 6 | 3 |
| `green_floor` | 8, 6 | 4 |
| `purple_floor` | 12, 6 | 4 |
| `ice` ✅ | 4, 7 | 5 |
| `cracked_ice` ✅ | 5, 7 | 1 |
| `ice_se` ✅ | 6, 7 | 1 |
| `ice_sw` ✅ | 7, 7 | 1 |
| `green_wall` | 8, 7 | 4 |
| `purple_wall` | 12, 7 | 4 |
| `force_floor_n` | 0, 8 | 1 |
| `force_floor_e` | 3, 8 | 1 |
| `ice_ne` ✅ | 6, 8 | 1 |
| `ice_nw` | 7, 8 | 1 |
| `railroad` | 8, 8 | 20 |
| `swivel_floor` | 15, 8 | 1 |
| `force_floor_s` | 1, 9 | 1 |
| `force_floor_w` | 2, 9 | 1 |
| `swivel_se` | 14, 9 | 1 |
| `swivel_sw` | 15, 9 | 1 |
| `force_floor_all` | 0, 10 | 8 |
| `swivel_ne` | 14, 10 | 1 |
| `swivel_nw` | 15, 10 | 1 |
| `slime` | 0, 11 | 8 |
| `dash_floor` | 8, 11 | 8 |
| `conveyor_n` | 12, 12 | 4 |
| `floor_ankh` | 10, 13 | 1 |
| `conveyor_e` | 12, 13 | 4 |
| `railroad_sign` | 4, 14 | 1 |
| `conveyor_s` | 12, 14 | 4 |
| `conveyor_w` | 12, 15 | 4 |
| `electrified_floor` | 12, 18 | 4 |
| `sokoban_wall` | 14, 20 | 4 |
| `sokoban_floor` | 15, 20 | 4 |
| `dirt_block` | 0, 24 | 2 |
| `ice_block` | 1, 24 | 2 |
| `floor_mimic` | 16, 26 | 1 |
| `splash_slime` | 16, 30 | 4 |

## hazard

| tile | col,row | cells |
|---|---|---|
| `water` ✅ | 0, 6 | 4 |
| `fire` ✅ | 0, 7 | 4 |
| `fire_boots` | 5, 12 | 1 |
| `bucket_water` | 8, 15 | 1 |
| `bucket_fire` | 9, 15 | 1 |
| `flame_jet_off` | 12, 17 | 1 |
| `flame_jet_on` | 13, 17 | 3 |
| `fireball` | 16, 25 | 4 |
| `bogus_player_burned_fire` | 17, 26 | 1 |

## key/door

| tile | col,row | cells |
|---|---|---|
| `key_red` | 0, 16 | 1 |
| `door_red` | 1, 16 | 1 |
| `gate_red` | 2, 16 | 1 |
| `key_blue` | 0, 17 | 1 |
| `door_blue` | 1, 17 | 1 |
| `gate_blue` | 2, 17 | 1 |
| `key_yellow` | 0, 18 | 1 |
| `door_yellow` | 1, 18 | 1 |
| `gate_yellow` | 2, 18 | 1 |
| `key_green` | 0, 19 | 1 |
| `door_green` | 1, 19 | 1 |
| `gate_green` | 2, 19 | 1 |

## item

| tile | col,row | cells |
|---|---|---|
| `chip` | 0, 12 | 3 |
| `chip_extra` | 3, 12 | 1 |
| `flippers` | 4, 12 | 1 |
| `cleats` | 6, 12 | 1 |
| `suction_boots` | 7, 12 | 1 |
| `no_sign` | 8, 12 | 1 |
| `gift_bow` | 9, 12 | 1 |
| `toll_gate` | 10, 12 | 1 |
| `dormant_bomb` | 11, 12 | 1 |
| `green_chip` | 0, 13 | 3 |
| `green_bomb` | 3, 13 | 1 |
| `hiking_boots` | 4, 13 | 1 |
| `lightning_bolt` | 5, 13 | 1 |
| `speed_boots` | 6, 13 | 1 |
| `bribe` | 7, 13 | 1 |
| `skeleton_key` | 8, 13 | 1 |
| `ankh` | 9, 13 | 1 |
| `phantom_ring` | 11, 13 | 1 |
| `score_10` | 0, 14 | 1 |
| `score_100` | 1, 14 | 1 |
| `score_1000` | 2, 14 | 1 |
| `score_2x` | 3, 14 | 1 |
| `hook` | 5, 14 | 1 |
| `foil` | 6, 14 | 1 |
| `xray_eye` | 7, 14 | 1 |
| `feather` | 8, 14 | 1 |
| `dumbbell` | 9, 14 | 1 |
| `remote_gray` | 10, 14 | 1 |
| `remote_green` | 11, 14 | 1 |
| `stopwatch_bonus` | 0, 15 | 1 |
| `stopwatch_penalty` | 1, 15 | 1 |
| `stopwatch_toggle` | 2, 15 | 1 |
| `score_5x` | 3, 15 | 1 |
| `helmet` | 4, 15 | 1 |
| `bowling_ball` | 5, 15 | 1 |
| `dynamite` | 6, 15 | 1 |
| `bomb` | 7, 15 | 1 |
| `nega_chip` | 13, 19 | 3 |
| `dynamite_lit` | 27, 27 | 5 |

## mechanism

| tile | col,row | cells |
|---|---|---|
| `exit` | 0, 4 | 4 |
| `socket` | 4, 4 | 1 |
| `no_player1_sign` | 5, 4 | 1 |
| `thief_tools` | 6, 4 | 1 |
| `thief_lock` | 7, 4 | 1 |
| `doppelganger1` | 2, 5 | 1 |
| `doppelganger2` | 2, 5 | 1 |
| `no_player2_sign` | 5, 5 | 1 |
| `thief_keys` | 6, 5 | 1 |
| `teleport_red` | 4, 16 | 4 |
| `transmogrifier` | 8, 16 | 5 |
| `teleport_rainbow` | 12, 16 | 4 |
| `teleport_blue` | 4, 17 | 4 |
| `turntable_ccw` | 8, 17 | 4 |
| `teleport_yellow` | 4, 18 | 4 |
| `turntable_cw` | 8, 18 | 4 |
| `teleport_green` | 4, 19 | 4 |
| `teleport_blue_exit` | 8, 19 | 1 |
| `button_blue` | 0, 20 | 2 |
| `button_green` | 1, 20 | 2 |
| `button_red` | 2, 20 | 2 |
| `button_brown` | 3, 20 | 2 |
| `button_pink` | 4, 20 | 2 |
| `button_black` | 5, 20 | 2 |
| `button_orange` | 6, 20 | 2 |
| `button_gray` | 7, 20 | 2 |
| `sokoban_block` | 9, 20 | 12 |
| `sokoban_button` | 12, 20 | 8 |
| `cloner` | 0, 22 | 1 |
| `trap` | 1, 22 | 2 |
| `scanner` | 2, 22 | 1 |
| `button_cyan` | 5, 22 | 2 |
| `light_switch_off` | 6, 22 | 2 |
| `button_yellow` | 7, 22 | 1 |
| `light_switch_on` | 6, 23 | 2 |
| `logic_gate` | 4, 28 | 42 |
| `player1_exit` | 28, 28 | 4 |
| `teleport_flash` | 20, 29 | 4 |
| `player2_exit` | 28, 29 | 4 |

## block

| tile | col,row | cells |
|---|---|---|
| `frame_block` | 2, 24 | 2 |
| `boulder` | 4, 24 | 7 |
| `log` | 8, 24 | 22 |
| `burr` | 4, 25 | 1 |
| `circuit_block` | 0, 26 | 3 |
| `glass_block` | 3, 26 | 1 |
| `green_block` | 0, 27 | 4 |

## player

| tile | col,row | cells |
|---|---|---|
| `player` | 16, 0 | 65 |
| `bogus_player_swimming` | 24, 0 | 4 |
| `player2` | 16, 4 | 65 |
| `bogus_player_drowned` | 17, 27 | 1 |

## monster

| tile | col,row | cells |
|---|---|---|
| `tank_blue` | 16, 8 | 8 |
| `tank_yellow` | 18, 8 | 8 |
| `bug` | 20, 8 | 16 |
| `paramecium` | 24, 8 | 12 |
| `glider` | 27, 8 | 8 |
| `ghost` | 29, 8 | 12 |
| `blob` | 16, 12 | 32 |
| `walker` | 24, 12 | 8 |
| `bear` | 26, 12 | 4 |
| `green_twister` | 30, 13 | 1 |
| `shark` | 31, 13 | 1 |
| `bull` | 29, 14 | 1 |
| `teeth` | 16, 16 | 12 |
| `teeth_timid` | 19, 16 | 12 |
| `glint` | 22, 16 | 24 |
| `rover` | 16, 24 | 11 |
| `ball` | 27, 24 | 5 |
| `rolling_ball` | 27, 25 | 10 |

## effect

| tile | col,row | cells |
|---|---|---|
| `explosion` | 16, 28 | 4 |
| `transmogrify_flash` | 20, 28 | 7 |
| `splash` | 16, 29 | 4 |
| `puff` | 24, 29 | 4 |
| `resurrection` | 28, 30 | 4 |
| `fall` | 16, 31 | 4 |
