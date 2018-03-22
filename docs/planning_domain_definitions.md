# Planning Domain Definitions

In this document, definitions for planning domains are defined for the later on 
symbolic planning. Symbolic planning shall be defined in 
[Planning Domain Definition Language (PDDL)](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language), 
so the definitions in the following sections will maximumly follow the PDDL 
syntax for convenience.


## Generic Objects

Below are generic objects that may occur in the game.

  * __Actor__: something that is controlled by the player
  * __Ground__: something that the __actor__ can stand on
  * __Ladder__: something that the __actor__ can climb on
  * __Chain__: something that the __actor__ can jump onto and climb on
  * __Conveyor__: something that the __actor__ can stand on which the __actor__ 
                  will be moved automatically
  * __Key__: something that can be picked up by the __actor__ and used to open 
             a __door__
  * __Door__: something that will stopped the __actor__ from moving forward, 
              and can be opened with a __key__
  * __Sword__: something that can be picked up by the __actor__ and used to 
               kill a __monster__
  * __Monster__: something that can kill the __actor__ when touching it, or be 
                 killed when the __actor__ is equipped with a __sword__
    - __Skull__: something that looks like a skull being a kind of __monsters__
    - __Snake__: something that looks like a snake being a kind of __monsters__
    - __Spider__: something that looks like a spider being a kind of 
                  __monsters__


## Predicates Definitions

Below are predicates (symbolic states) definitions that can be monitored:

  * `(actorInRoom ?room)`: assert if the actor is in a room
    - `?room`: the name of a room
  * `(actorOnSpot ?room ?spot)`: assert if the actor is on a spot in a room
    - `?room`: the name of a room
    - `?spot`: the name of an spot in the room, whose name prefix can be 
      `ladder`, `chain`, `conveyor`, `entrance` or `landmark`
  * `(keyExists ?room ?key)`: assert if a key exists (not been taken) in a room 
    - `?room`: the name of a room
    - `?key`: the name of a key in the room
  * `(actorWithKey)`: assert if the actor is with a key
  * `(swordExists ?room ?sword)`: assert if a sword exists (not been taken) in 
    a room 
    - `?room`: the name of a room
    - `?sword`: the name of a sword in the room
  * `(actorWithSword)`: assert if the actor is with a sword
  * `(doorExists ?room ?door)`: assert if a door exists (not been open) in a 
    room
    - `?room`: the name of a room
    - `?door`: the name of a door in the room
  * `(monsterExists ?room ?monster)`: assert if a monster exists (not been 
    killed or destoryed) in the room
    - `?room`: the name of a room
    - `?monster`: the name of a monster in the room, whose name prefix can be 
      `skull` `snake` or `spider`

Below are predicates (symbolic states) definitions that are pre-defined as 
environmental configurations:

  * `(pathExists ?roomFrom ?positionFrom ?roomTo ?positionTo)`: assert if a 
    path exists from a position in a room to another position in a room
    - `?roomFrom`: the name of the initial room
    - `?positionFrom`: the name of an initial position in the initial room
    - `?roomTo`: the name of the destination room
    - `?positionTo`: the name of a destination position in the destination room

Note that for the purpose of being consistent in naming, the object defined by 
number shall be named from top-left to bottom-right starting from `1`. For 
example, a room with `4` objects of the same kind as `key` shall be named in 
the following way:

  ```
  key_1 key_2
  key_3 key_4
  ```


## References:

  * [An Introduction to PDDL](https://www.cs.toronto.edu/~sheila/2542/s14/A1/introtopddl2.pdf)
  * [PDDL Editor](http://editor.planning.domains)
  * [Beating Atari with Natural Language Guided Reinforcement Learning](https://arxiv.org/abs/1704.05539)


