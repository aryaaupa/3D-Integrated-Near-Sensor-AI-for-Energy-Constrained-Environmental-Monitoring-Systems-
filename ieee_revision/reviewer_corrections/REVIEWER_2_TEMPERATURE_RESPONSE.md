# Reviewer 2: sensing accuracy versus temperature

## Evidence decision

No accuracy-versus-temperature curve can be generated from the present
evidence.

The repository and supplied manuscript were checked for all of the following:

- temperature-labeled sensor observations;
- sensor modality and transducer transfer function;
- ground-truth labels;
- trained-model checkpoints or predictions;
- per-temperature correct/incorrect counts;
- confusion matrices or classwise metrics;
- a calibration procedure connecting temperature to sensor output.

None are present. The available temperature information is limited to the
nominal 27 °C device-model temperature in the PTM/ngspice link simulation and
qualitative discussion of 3D-stack thermal management. Timeloop and Accelergy
do not generate sensing predictions. Sweeping `.temp` in ngspice could
characterize circuit energy or delay, but it cannot produce sensing accuracy.
No curve is therefore created.

## Reviewer-response draft

> **Reviewer 2 comment:** Please quantify sensing accuracy as a function of
> temperature and clarify the thermal implications of the proposed stack.
>
> **Response:** We thank the reviewer and agree that temperature-dependent
> sensing accuracy is important for a deployable near-sensor system. The
> present study evaluates the compute and memory architecture, using
> Timeloop/Accelergy for workload mapping, memory activity, cycles,
> utilization, and component energy, together with a complementary ngspice
> evaluation of a representative communication link. It does not select or
> model a specific sensing transducer, and the available repository contains
> no temperature-labeled sensing dataset, ground-truth labels, or calibrated
> sensor/model response from which an accuracy-versus-temperature curve could
> be computed. We therefore did not add a synthetic curve. Instead, we revised
> the manuscript to remove statements implying demonstrated thermal isolation
> or temperature-robust sensing accuracy, explicitly identify this limitation,
> and discuss temperature-dependent sensing validation as required future
> work. The thermal section now treats vertical thermal coupling, tier
> ordering, coordinated core-memory power regulation, and heat removal as
> physical-design requirements rather than demonstrated benefits of the
> evaluated architecture.
>
> **Location in revised manuscript:** Section VI, Physical-Design and Thermal
> Considerations; Section VII, Limitations and Future Validation.

## Manuscript replacement text

> The present evaluation does not quantify sensing accuracy as a function of
> temperature. Such a result requires a specified transducer, calibrated
> temperature-dependent sensor measurements, labeled inference data, and a
> fixed accuracy metric; these inputs are outside the current Timeloop,
> Accelergy, CACTI, and link-level ngspice models. Accordingly, no relationship
> between stack temperature and sensing accuracy is inferred from the reported
> energy results. Vertical thermal coupling, tier ordering, heat spreading,
> and coordinated compute-memory power management remain physical-design
> requirements for a future implementation. A complete validation should
> measure the selected sensor and end-to-end inference pipeline over a
> controlled temperature range, report sample counts and uncertainty at each
> temperature, and distinguish sensor drift from electronic timing or memory
> effects.

## Statements in the supplied manuscript that must be removed or rewritten

The supplied draft contains unsupported statements that go beyond the
available evidence, including claims that:

- the memory tier acts as a thermal barrier;
- layer placement preserves sensor signal fidelity;
- reduced data movement consequently lowers steady-state temperature;
- workload distribution improves thermal uniformity;
- the architecture mitigates thermal challenges without compromising
  reliability;
- thermal-aware placement has been shown by the present results to be
  effective.

These may be discussed only as hypotheses, design considerations, or future
work. They are not results of the current simulations.

## Minimum experiment needed for a future curve

A defensible accuracy-versus-temperature curve would require, at minimum:

1. one explicitly named sensor/transducer and acquisition chain;
2. a controlled temperature protocol and measured device temperature;
3. the same labeled evaluation samples at every temperature;
4. a frozen preprocessing and inference model;
5. raw predictions and ground truth;
6. a prespecified metric such as balanced accuracy or F1 score;
7. sample count, confidence intervals, and repeated trials at each point;
8. separate reporting of sensor drift, circuit failure, and model error.

Literature values from a different sensor cannot be relabeled as measured or
simulated accuracy of the proposed system.
