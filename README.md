# ICEBERG

The `master` branch generally reflects the ICEBERG release on Pypi, and is
considered stable: it should work 'out of the box'. Please refer to the documentation.

The `devel` branch (and any other branches than master, for that matter)
may not correspond to the published documentation, and specifically may have
dependencies which need to be resolved manually.  Please contact us with an issue
if you need advice on the usage of any non-master branch.

[![Devel Build Status](https://travis-ci.com/iceberg-project/ICEBERG-middleware.svg?branch=devel)](https://travis-ci.com/iceberg-project/ICEBERG-middleware) [![codecov](https://codecov.io/gh/iceberg-project/ICEBERG-middleware/branch/devel/graph/badge.svg)](https://codecov.io/gh/iceberg-project/ICEBERG-middleware)

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

Before using ICEBERG a connection to a MongoDB is needed. To setup a password 
protected database through Docker, see [instructions here](https://hackernoon.com/securing-mongodb-on-your-server-1fc50bd1267b)
Then export the following variable

```bash
export RADICAL_PILOT_DBURL=mongodb://usernane:password@mongodb_hostname:port/db_name
export RMQ_ENDPOINT=ip_value
export RMQ_PORT=port_number
export VE_SEALS=ve_path/ve_name
```

The ICEBERG command can be executed as follows:
```bash
iceberg [-h] [--resource RESOURCE] [--queue QUEUE] [--cpus CPUS]
               [--gpus GPUS] [--input_path INPUT_PATH]
               [--output_path OUTPUT_PATH] [--walltime WALLTIME]
               [--analysis ANALYSIS]
               {seals,penguins,4Dgeolocation,rivers,landcover} ...
               
```

The arguments shown are mandatory for the command to execute correctly. Executing with `-h` will
provide the following response:
```

positional arguments:
  {seals,penguins,4Dgeolocation,rivers,landcover}

optional arguments:
  -h, --help            show this help message and exit

Required Arguments:
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
```

The expected analysis commands are:
1. seals
2. penguins
3. 4DGeolocation
4. landcover
5. rivers

Based on the selected analysis further arguments may be required. 

To see further help messages per use case execute the ICEBERG command with all the arguments
and add a `--help` after it. It will print the arguments for the selected alanysis.
