# Three-hour generator scheduling

A microgrid must meet its electricity demand in each of three one-hour periods. It has two generators, A and B. The operating limits and costs are given in [units.csv](units.csv), and the demand for each hour is given in [demand.csv](demand.csv).

In each hour, a generator is either off, with zero output, or on, producing an integer number of megawatts within its inclusive operating bounds. An operating generator incurs the fixed cost for that hour plus the per-MW cost multiplied by its output. The two outputs must add up to the demand exactly. Hours are independent.

1. **Base schedule.** Find the minimum-cost schedule. Report each generator's output and the cost for every hour, plus the total cost.
2. **Demand scenario.** Increase demand by 10 MW in every hour. Reuse the same cost and operating rules. Report the revised schedule and compare its total cost with the base schedule.
3. **Feasibility check.** Return to the original demand in hours 1 and 3 and replace the hour 2 demand with 141 MW. State whether a feasible schedule exists and justify your answer.

Write a short English report with your model, schedule tables, checks and the scope of your conclusions.
