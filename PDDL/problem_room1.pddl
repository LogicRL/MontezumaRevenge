;; problem definition for room 1

(define (problem ProblemMontezumaRevengeRoom1)

    (:domain MontezumaRevenge)
    
    (:objects
        room_1 - room 
        entrance_1 entrance_2 - spot
        ladder_1 ladder_2 ladder_3 - spot
        conveyor_1 - spot
        chain_1 - spot
        door_1 door_2 - door
        key_1 - key
        skull_1 - monster
    )
    
    (:init
        ; configuration: paths from entrance_1
        (doorPathExists room_1 entrance_1 door_1 room_1 ladder_1)
        ; configuration: paths from ladder_1
        (doorPathExists room_1 ladder_1 door_1 room_1 entrance_1)
        (pathExists room_1 ladder_1 room_1 conveyor_1)
        (doorPathExists room_1 ladder_1 door_2 room_1 entrance_2)
        ; configuration: paths from entrance_2
        (doorPathExists room_1 entrance_2 door_2 room_1 ladder_1)
        ; configuration: paths from key_1
        (pathExists room_1 key_1 room_1 ladder_3)
        ; configuration: paths from chain_1
        (pathExists room_1 chain_1 room_1 conveyor_1)
        (pathExists room_1 chain_1 room_1 ladder_2)
        ; configuration: paths from ladder_3
        (pathExists room_1 ladder_3 room_1 key_1)
        (pathExists room_1 ladder_3 room_1 ladder_2)
        ; configuration: paths from conveyor_1
        (pathExists room_1 conveyor_1 room_1 ladder_1)
        (pathExists room_1 conveyor_1 room_1 chain_1)
        ; configuration: paths from ladder_2
        (pathExists room_1 ladder_2 room_1 chain_1)
        (pathExists room_1 ladder_2 room_1 ladder_3)
        ; initial states
        (actorOnSpot room_1 ladder_1)
        (keyExists room_1 key_1)
        (doorExists room_1 door_1)
        (doorExists room_1 door_2)
        (monsterExists room_1 skull_1)
    )
    
    (:goal
        (actorOnSpot room_1 entrance_1)
    )
)
