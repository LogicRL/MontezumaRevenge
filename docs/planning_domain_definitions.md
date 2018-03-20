# Planning Domain Definitions

In this document, definitions for planning domains are defined for the later on 
symbolic planning. Symbolic planning shall be defined in 
[Planning Domain Definition Language (PDDL)](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language), 
so the definitions in the following sections will maximumly follow the PDDL 
syntax for convenience.


## Generic Objects

Below are generic objects that may occur in the game.

  * __Actor__: the actor that is controlled by the player
  * __Ground__: the ground that the actor can stand on
  * __Ladder__: the ladder that the actor can climb on
  * __Rope__: the rope that the actor can jump onto and climb on
  * __Key__: the key that can be picked up by the actor and used to open a door
  * __Door__: the door that will stopped the actor from moving forward, and can 
              be opened with a key
  * __Sword__: the sword that can be picked up by the actor and used to kill an 
               enemy
  * __Monster__: the monster that can kill the actor when touching the actor, 
                 or be killed when the actor is equipped with a sword
    - __Ghost__: the ghost being a kind of monsters
    - __Snake__: the snake being a kind of monsters


## Predicates Definitions

Below are predicates (symbolic states) definitions that can be monitored:

  * `(actorInRoom ?room)`: assert if the actor is in room `?room`
    - `?room`: the name of a room
  * `(actorOnSpot ?room ?spot)`: assert if the actor is on a spot in a room
    - `?room`: the name of a room
    - `?spot`: the name of an spot in the room, whose name prefix can be 
      `ladder`, `chain`, `conveyor`, `entrance` or `landmark`
  * `(keyExists ?room ?key)`: assert if a key exists (not been taken) in a room 
    - `?room`: the name of a room
    - `?key`: the name of a key in the room
  * `(actorWithKey)`: assert if the actor is with a key
  * `(doorExists ?room ?door)`: assert if a door exists (not been open) in a 
    room is open
    - `?room`: the name of a room
    - `?door`: the name of a door in the room
  * `(monsterExists ?room ?monster)`: assert if a monster exists (not been 
    killed or destoryed) in the room
    - `?room`: the name of a room
    - `?monster`: the name of a monster in the room, whose name prefix can be 
      `skull` `snake` or `spider`

Below are predicates (symbolic states) definitions that are pre-defined as 
environmental configurations:

  * `(pathExists ?roomFrom ?spotFrom ?roomTo ?spotTo)`: assert if a path exists 
    from a spot in a room to another spot in a room
    - `?roomFrom`: the name of the initial room
    - `?spotFrom`: the name of an initial spot in the initial room
    - `?roomTo`: the name of the destination room
    - `?spotTo`: the name of a destination spot in the destination room

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


