;; domain definition for Montezuma Revenge environment

(define (domain MontezumaRevenge)

    (:requirements
        :durative-actions
        :equality
        :negative-preconditions
    ;    :numeric-fluents
    ;    :object-fluents
        :typing
    )

    (:types
        room
        position
        spot - position
        obtainable - position
        carriable - obtainable
        key - carriable
        sword - carriable
        reward - obtainable
        door - position
        monster
    )

    (:constants

    )

    (:predicates
        (actorOnSpot ?room - room ?spot - spot)
        (keyExists ?room - room ?key - key)
        (actorWithKey)
        (swordExists ?room - room ?sword - sword)
        (actorWithSword)
        (rewardExists ?room - room ?reward - reward)
        (doorExists ?room - room ?door - door)
        (monsterExists ?room - room ?monster - monster)
        (pathExists ?roomFrom - room ?positionFrom - position ?roomTo - room ?positionTo - position)
        (doorPathExists ?roomFrom - room ?positionFrom - position ?door - door ?roomTo - room ?positionTo - position)
    )

    (:functions

    )

    (:action moveActor
        ; move the actor from a spot in a room to another spot in a room
        :parameters (?roomFrom - room ?spotFrom - spot ?roomTo - room ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?roomFrom ?spotFrom)
            (not (actorOnSpot ?roomTo ?spotTo))
            (pathExists ?roomFrom ?spotFrom ?roomTo ?spotTo)
        )
        :effect (and
            (actorOnSpot ?roomTo ?spotTo)
            (not (actorOnSpot ?roomFrom ?spotFrom))
        )
    )
    
    (:action moveActorThroughClosedDoor
        ; move the actor from a spot in a room to another spot in a room through 
        ; a closed door
        :parameters (?roomFrom - room ?spotFrom - spot ?door - door ?roomTo - room ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?roomFrom ?spotFrom)
            (not (actorOnSpot ?roomTo ?spotTo))
            (doorPathExists ?roomFrom ?positionFrom ?door ?roomTo ?positionTo)
            (doorExists ?door)
            (actorWithKey)
        )
        :effect (and
            (not (doorExists ?door))
            (not (actorWithKey))
            (actorOnSpot ?roomTo ?spotTo)
            (not (actorOnSpot ?roomFrom ?spotFrom))
        )
    )
    
    (:action moveActorThroughOpenDoor
        ; move the actor from a spot in a room to another spot in a room through 
        ; a open door
        :parameters (?roomFrom - room ?spotFrom - spot ?door - door ?roomTo - room ?spotTo - spot)
        :precondition (and
            (actorOnSpot ?roomFrom ?spotFrom)
            (not (actorOnSpot ?roomTo ?spotTo))
            (doorPathExists ?roomFrom ?positionFrom ?door ?roomTo ?positionTo)
            (not (doorExists ?door))
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
            (pathExists ?room ?spot ?room ?key)
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
            (pathExists ?room ?spot ?room ?sword)
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
            (pathExists ?room ?spot ?room ?reward)
        )
        :effect (and
            (not (rewardExists ?room ?reward))
        )
    )
)
