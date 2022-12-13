# Flowrence

Introducing Flowrence - a Bayesian framework for optimising traffic flow in cities.

## Installation

It is recommended to use a virtual environment for this project. First, clone the repository:

```
git clone git@github.com:yu202147657/L48_Traffic.git && cd L48_Traffic
```

Then create and activate the venv:

```
python3 -m venv .venv
source .venv/bin/activate
```

You may need to `apt install python3.10-venv`, if this command fails, before retrying. The virtual env can be deactivated by running `deactivate` in the terminal.


### Setting up CityFlow

CityFlow is the traffic simulator used for this project. It can be installed with the following commands (taken from the CityFlow installation guide):

```
sudo apt update && sudo apt install -y build-essential cmake
git clone https://github.com/cityflow-project/CityFlow.git
pip install ./CityFlow
```

The project's requirements can now be installed using

```
pip install -r requirements.txt
```


