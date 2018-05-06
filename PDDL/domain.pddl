;; domain definition for Montezuma Revenge environment

(define (domain MontezumaRevenge)

    (:requirements
    ;    :durative-actions
    ;    :equality
    ;    :negative-preconditions
    ;    :numeric-fluents
    ;    :object-fluents
        :typing
    )

    (:types room spot key sword reward door monster)

    ; (:constants
    ; 
    ; )

    (:predicates
        (actorOnSpot ?room - room ?spot - spot)
        (keyExists ?room - room ?key - key)
        (actorWithKey)
        (swordExists ?room - room ?sword - sword)
        (actorWithSword)
        (actorRevivesOnSpot ?room - room ?revivingSpot - spot)
        (rewardExists ?room - room ?reward - reward)
        (doorExists ?room - room ?door - door)
        (monsterExists ?room - room ?monster - monster)
        (keyReachable ?room - room ?spot - spot ?key - key)
        (swordReachable ?room - room ?spot - spot ?sword - sword)
        (rewardReachable ?room - room ?spot - spot ?reward - reward)
        (monsterReachable ?room - room ?spot - spot ?monster - monster)
        (pathExistsInRoom ?room - room ?spotFrom - spot ?spotTo - spot)
        (doorPathExistsInRoom ?room - room ?spotFrom - spot ?door - door ?spotTo - spot)
        (monsterPathExistsInRoom ?room - room ?spotFrom - spot ?monster - monster ?spotTo - spot)
        (pathExistsAcrossRooms ?roomFrom - room ?spotFrom - spot ?roomTo - room ?spotTo - spot)
    )

    ; (:functions
    ; 
    ; )

    (:action moveActorInRoom
        ; move the actor from a spot to another spot in a room
        :parameters (?room - room ?spotFrom - spot ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?room ?spotFrom)
            (not (actorOnSpot ?room ?spotTo))
            (pathExistsInRoom ?room ?spotFrom ?spotTo)
        )
        :effect (and
            (actorOnSpot ?room ?spotTo)
            (not (actorOnSpot ?room ?spotFrom))
        )
    )
    
    (:action moveActorInRoomThroughClosedDoor
        ; move the actor from a spot to another spot through a closed door in a 
        ; room
        :parameters (?room - room ?spotFrom - spot ?door - door ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?room ?spotFrom)
            (not (actorOnSpot ?room ?spotTo))
            (doorPathExistsInRoom ?room ?spotFrom ?door ?spotTo)
            (doorExists ?room ?door)
            (actorWithKey)
        )
        :effect (and
            (not (doorExists ?room ?door))
            (not (actorWithKey))
            (actorOnSpot ?room ?spotTo)
            (not (actorOnSpot ?room ?spotFrom))
        )
    )
    
    (:action moveActorInRoomThroughOpenDoor
        ; move the actor from a spot to another spot through an open door in a 
        ; room 
        :parameters (?room - room ?spotFrom - spot ?door - door ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?room ?spotFrom)
            (not (actorOnSpot ?room ?spotTo))
            (doorPathExistsInRoom ?room ?spotFrom ?door ?spotTo)
            (not (doorExists ?room ?door))
        )
        :effect (and
            (actorOnSpot ?room ?spotTo)
            (not (actorOnSpot ?room ?spotFrom))
        )
    )

    (:action moveActorInRoomThroughDeadMonster
        ; move the actor from a spot to another spot through a dead monster in 
        ; a room 
        :parameters (?room - room ?spotFrom - spot ?monster - monster ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?room ?spotFrom)
            (not (actorOnSpot ?room ?spotTo))
            (monsterPathExistsInRoom ?room ?spotFrom ?monster ?spotTo)
            (not (monsterExists ?room ?monster))
        )
        :effect (and
            (actorOnSpot ?room ?spotTo)
            (not (actorOnSpot ?room ?spotFrom))
        )
    )
    
    (:action moveActorAcrossRooms
        ; move the actor from a spot in a room to another spot in another room
        :parameters (?roomFrom - room ?spotFrom - spot ?roomTo - room ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?roomFrom ?spotFrom)
            (not (actorOnSpot ?roomTo ?spotTo))
            (pathExistsAcrossRooms ?roomFrom ?spotFrom ?roomTo ?spotTo)
        )
        :effect (and
            (actorOnSpot ?roomTo ?spotTo)
            (not (actorOnSpot ?roomFrom ?spotFrom))
        )
    )
    
    (:action grabKey
        ; grab a key from a spot
        :parameters (?room - room ?spot - spot ?key - key)
        :precondition (and
            (actorOnSpot ?room ?spot)
            (keyExists ?room ?key)
            (keyReachable ?room ?spot ?key)
            (not (actorWithKey))
        )
        :effect (and
            (actorWithKey)
            (not (keyExists ?room ?key))
        )
    )
    
    (:action grabSword
        ; grab a sword from a spot
        :parameters (?room - room ?spot - spot ?sword - sword)
        :precondition (and
            (actorOnSpot ?room ?spot)
            (swordExists ?room ?sword)
            (swordReachable ?room ?spot ?sword)
            (not (actorWithSword))
        )
        :effect (and
            (actorWithSword)
            (not (swordExists ?room ?sword))
        )
    )
    
    (:action grabReward
        ; grab a reward from a spot
        :parameters (?room - room ?spot - spot ?reward - reward)
        :precondition (and
            (actorOnSpot ?room ?spot)
            (rewardExists ?room ?reward)
            (rewardReachable ?room ?spot ?reward)
        )
        :effect (and
            (not (rewardExists ?room ?reward))
        )
    )

    (:action suicideWithMonster
        ; sucide with a monster from a spot
        :parameters (?room - room ?spot - spot ?monster - monster ?revivingSpot - spot)
        :precondition (and
            (actorOnSpot ?room ?spot)
            (monsterExists ?room ?monster)
            (monsterReachable ?room ?spot ?monster)
            (actorRevivesOnSpot ?room ?revivingSpot)
        )
        :effect (and
            (not (monsterExists ?room ?monster))
            (not (actorOnSpot ?room ?spot))
            (actorOnSpot ?room ?revivingSpot)
        )
    )
)
