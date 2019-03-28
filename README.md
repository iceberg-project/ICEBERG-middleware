# ICEBERG

The `master` branch generally reflects the ICEBERG release on Pypi, and is
considered stable: it should work 'out of the box'. Please refer to the documentation.

The `devel` branch (and any other branches than master, for that matter)
may not correspond to the publised documentation, and specifically may have
dependencies which need to be resolved manually.  Please contact us with an issue
if you need advice on the usage of any non-master branch.

## Installation:

To install our package you should clone the repo by running and checkout the `devel` branch:
```bash
git clone https://github.com/ICEBERG-project/ICEBERG-middleware.git
git checkout devel
```

Then create a Python Virtual Environment ([VirtualEnv](https://virtualenv.pypa.io/en/latest/) or
[Conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html?))
and move in the ICEBERG-middleware folder.

To install run:
```bash
pip install . --upgrade
```

## Usage

The ICEBERG command can be executed as follows:
```bash
iceberg [-h] --resource RESOURCE --queue QUEUE --cpus CPUS --gpus GPUS
               --input_path INPUT_PATH --output_path OUTPUT_PATH --walltime
               WALLTIME --analysis ANALYSIS [<args>]
```

The arguments shown are mandatory for the command to execute correctly. Executing with `-h` will
provide the following responce:
```
  --resource RESOURCE, -r RESOURCE
                        Where the execution will happen
  --queue QUEUE, -q QUEUE
                        The queue of the resource
  --cpus CPUS, -c CPUS  How many CPUs will be required
  --gpus GPUS, -g GPUS  How many GPUs will be required
  --input_path INPUT_PATH, -ip INPUT_PATH
                        Where the input images are
  --output_path OUTPUT_PATH, -op OUTPUT_PATH
                        Where the results should be saved
  --walltime WALLTIME, -w WALLTIME
                        The estimated execution time
  --analysis ANALYSIS, -a ANALYSIS
                        The type of analysis to be executed
```

The expected analysis option takes can take the following values:
1. seals
2. penguins
3. 4DGeolocation
4. landcover
5. rivers

Based on the selected analysis further arguments may be required. 

To see further help messages per use case execute the ICEBERG command with all the arguments
and add a `--help` after it. It will print the arguments for the selected alanysis.