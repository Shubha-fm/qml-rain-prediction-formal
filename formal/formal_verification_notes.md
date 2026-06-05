# Formal Verification Notes

The formal layer models the decision behavior after the QML model produces a rain probability.

## Informal requirement

If the weather condition has high risk, the system should not remain in `NoWarning`.

## Variables

- `humidity`: input humidity value from 0 to 100
- `cloud`: cloud cover value from 0 to 100
- `prob`: rain probability from 0 to 100
- `decision`: one of `NoWarning`, `Watch`, or `Warning`

## Safety properties

1. `TypeOK`: all variables remain in the valid range.
2. `DecisionValid`: the decision is always one of the allowed states.
3. `WarningSafety`: a high-risk condition should not be left without warning after the decision step.
4. `ReachWarning`: the warning state is reachable.

## How this connects to QML

The QML model estimates rain probability. The formal policy checks whether that probability is converted into a safe decision. This separation is useful because machine learning can be probabilistic, while the decision policy can still be checked using formal methods.

## TLC command

```bash
tlc tla/RainPrediction.tla -config tla/RainPrediction.cfg
```

Note: depending on the TLC setup, `WarningSafety` can be checked as an invariant after strengthening the model to force a decision after each prediction. The included model is intentionally simple for teaching and demonstration.
