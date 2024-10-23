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



### Processing for Real-World Datasets
We perform the following processing separately for each dataset:

- **Flu Outpatient:** The dataset is collected through the U.S. Outpatient Influenza-like Illness Surveillance Network (ILINET). It contains patient information for each week from $1997$ to $2023$. We select the `ILITOTAL` attribute for evaluation.
- **Flu Death:** This dataset is collected by The National Center for Health Statistics (NCHS). It records the number of deaths per week occurring in the United States from 2019 to 2023. We select the `NUM INFLUENZA DEATHS` attribute for evaluation.`
-  **Unemployment:** This dataset records the Unemployment Level of $16$-$19$ Yrs., Black or African American per month from $1972$ to $2023$. We use the `LNU03000018` attribute for evaluation. 
- **State Flu:** This dataset is collected by the same institution as the Flu Outpatient dataset and reflects the number of Influenza-like Illness in $55$ different regions across the US over time. Each dimension represents a region, and each column reflects the number of patients in that region during the period from $2010$ to $2023$.
- **TDrive:** This is a sample of T-Drive trajectory dataset that contains a one-week trajectories of $10,357$ taxis. We divide the trajectory range into regions of 0.1 longitude * 0.1 latitude and downsample to $64$ regions to count the number of taxis within each region at different times.
- **Retail:** This dataset contains historical sales data from $45$ stores. We reorganized and sampled the dataset into $100$ dimensions based on the different departments at different times for each store. Each dimension reflects the sales quantity of a department in a store at different timestamps.
