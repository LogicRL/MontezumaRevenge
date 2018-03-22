;; problem definition for room 1

(define (problem ProblemMontezumaRevengeRoom1)

    (:domain MontezumaRevenge)
    
    (:objects
        room_1 - room
        entrance_1 entrance_2 - spot
        ladder_1 ladder_2 ladder_3 - spot
        conveyor_1 conveyor_2 - spot
        chain_1 - spot
        door_1 door_2 - door
        key_1 - key
        skull_1 - monster
        reward_0 - reward
        sword_0 - sword
    )
    
    (:init
        ; configuration: paths from entrance_1
        (doorPathExistsInRoom room_1 entrance_1 door_1 ladder_1)
        ; configuration: paths from ladder_1
        (doorPathExistsInRoom room_1 ladder_1 door_1 entrance_1)
        (doorPathExistsInRoom room_1 ladder_1 door_2 entrance_2)
        (pathExistsInRoom room_1 ladder_1 conveyor_1)
        (pathExistsInRoom room_1 ladder_1 conveyor_2)
        ; configuration: paths from entrance_2
        (doorPathExistsInRoom room_1 entrance_2 door_2 ladder_1)
        ; configuration: paths from chain_1
        (pathExistsInRoom room_1 chain_1 conveyor_2)
        (pathExistsInRoom room_1 chain_1 ladder_2)
        ; configuration: paths from ladder_3
        (pathExistsInRoom room_1 ladder_3 ladder_2)
        (keyReachable room_1 ladder_3 key_1)
        ; configuration: paths from conveyor_1
        (pathExistsInRoom room_1 conveyor_1 ladder_1)
        (pathExistsInRoom room_1 conveyor_1 conveyor_2)
        ; configuration: paths from conveyor_2
        (pathExistsInRoom room_1 conveyor_2 ladder_1)
        (pathExistsInRoom room_1 conveyor_2 chain_1)
        (pathExistsInRoom room_1 conveyor_2 conveyor_1)
        ; configuration: paths from ladder_2
        (pathExistsInRoom room_1 ladder_2 chain_1)
        (pathExistsInRoom room_1 ladder_2 ladder_3)
        ; initial states
        (actorOnSpot room_1 ladder_1)
        (keyExists room_1 key_1)
        (doorExists room_1 door_1)
        (doorExists room_1 door_2)
        (monsterExists room_1 skull_1)
    )
    
    (:goal (and
        (actorOnSpot room_1 entrance_1)
    ))
)
