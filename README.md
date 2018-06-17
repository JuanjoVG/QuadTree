# QuadTree

## Tests

To execute the test of the project, execute the following line in a terminal from the project root directory:

```
python tests.py
```

## Experiments

To execute the designed experiment of the project, execute the following line in a terminal from the project root directory:

```
python experiment.py
```
These experiments can be tuned changing the parameters declared on the top of the file *experiment.py*:
```python
plot_filename = 'Timing.PNG'
test_sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
replications = 100

random.seed(24011994)
```
