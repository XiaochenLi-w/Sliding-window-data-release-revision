# SPAS: Continuous Release of Data Streams under w-Event Differential Privacy

Tested Python version: 3.11.4

numpy and matplotlib is required.


### Evaluation

To evaluate all methods for data release, run:
```
python ./evaluation/evaluate_all.py
```
To evaluate all methods for range query, run:

```
python ./evaluation/evaluate_range_query.py
```

The result will be saved automatically in `/output`.


### View in graph

To view the result in curve graph, you should first create a `fig` directory:
```
mkdir fig
```
Run 'draw_heat.py' for heat graph, run 'draw_radar' for radar graph.

For example:

```
python ./mechanism/draw_heat.py
```
The graph will be saved in `fig/` folder automatically.

