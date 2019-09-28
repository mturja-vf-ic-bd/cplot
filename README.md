# Circle Plot for Brain Network Visualization

## Input:
```
usage: main.py [-h] [-l] [-f INPUT_NET] [-o OUTFILE] c

CIRCLE PLOT FOR BRAIN NETWORK

positional arguments:
  c                     number of rings

optional arguments:
  -h, --help            show this help message and exit
  -l, --link            if true, shows links inside the circle
  -f INPUT_NET, --input_net INPUT_NET
                        input file for adjacency matrix
  -o OUTFILE, --outfile OUTFILE
                        output file for circle plot
 ```                  

```Example: 
To plot only 3 rings: python3 main.py 3
3 rings with links: python3 main.py 3 -l -f demo_network.txt
```

## Output:
![Result](demo_cplot.png)
