----------------------------- MODULE RainPrediction -----------------------------
EXTENDS Naturals, TLC

CONSTANTS Low, Medium, High

VARIABLES humidity, cloud, prob, decision

DecisionSet == {"NoWarning", "Watch", "Warning"}
RiskSet == {Low, Medium, High}

Init ==
    /\ humidity \in 0..100
    /\ cloud \in 0..100
    /\ prob \in 0..100
    /\ decision = "NoWarning"

Risk ==
    IF prob >= 70 /\ humidity >= 75 /\ cloud >= 60 THEN High
    ELSE IF prob >= 45 /\ humidity >= 60 THEN Medium
    ELSE Low

Predict ==
    /\ prob' \in 0..100
    /\ humidity' \in 0..100
    /\ cloud' \in 0..100
    /\ decision' = decision

Decide ==
    /\ UNCHANGED <<humidity, cloud, prob>>
    /\ decision' =
        IF Risk = High THEN "Warning"
        ELSE IF Risk = Medium THEN "Watch"
        ELSE "NoWarning"

Next == Predict \/ Decide

Spec == Init /\ [][Next]_<<humidity, cloud, prob, decision>>

TypeOK ==
    /\ humidity \in 0..100
    /\ cloud \in 0..100
    /\ prob \in 0..100
    /\ decision \in DecisionSet

WarningSafety ==
    Risk = High => decision # "NoWarning"

DecisionValid == decision \in DecisionSet

ReachWarning == <>(decision = "Warning")

=============================================================================
