
## Autonomous and Knowledge-based Synthetic Data Generation

This software adds an autonomy layer and an abstraction layer on top of BlenderProc.

With the autonomy layer:
* Programmers can program modules that define a form and API for a synthetic data generation pipeline
* Process Experts can influence the generation process via a web-based UI
* Other systemms can trigger trigger synthetic data generation via a REST API

With the abstraction layer:
* Algorithms are split from expert knowledge
* Algorithms become reusable
* It is saved how a dataset was created

## Installation

#### 1) Install required software

* Install Node.js (e.g., 16.14.2)
* Install Python (3.9)

#### 2) Install BlenderProc (globally) and required packages

* Start powershell
* Execute the following commands:

```
pip install blenderproc==2.4.0
blenderproc pip install owlready2
```

#### 3) Create and start a virtual environment (venv)

* Download this repository to your local drive
* Start powershell
* Navigate to ...\knowledge-based-synthetic-data-generation\
* Execute the following commands:

```
py -3 -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```

#### 4) Install core libraries

```
pip install flask
pip install owlready2
```

#### 5) Initialize database

```
flask --app my_package --debug init-db
```

#### 6) Install packages needed for frontend

* Navigate to ...\my_package\frontend\
* ```npm install```

## Starting the server

### Start Flask server in production mode

* Use a production server, e.g., [waitress](https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/)

#### 1) Install the production server package in the virtual environment (venv)

#### 2) Start the server using the respective production server's commands

#### 3) When starting the server, it's IP address will likely be printed (or it has to be found out in another way). Copy this address into the browser to access the web application (the ip address from the production server may be different from the debugging server).


### Start Flask server in debug mode

#### 1) Start virtual environment (venv) (if not still active)

* Navigate to ...\knowledge-based-synthetic-data-generation\
* Execute the following commands:

```
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```

#### 2) Start the flask server

```
flask --app my_package --debug run
```

* (--debug can be left away if changes in flask source code should not automatically be compiled)
* PLEASE NOTE: Running in debug note is not recommended for even small deployment. For instance, 3d model uploads often don't work here. Instead, please use production mode.

#### 3) When starting the server, it's IP address will be printed. Copy this address into the browser to access the web application


## Used software

| Software    | Licence     |
| ----------- | ----------- |
| [BlenderProc](https://github.com/DLR-RM/BlenderProc)      | GPL-3.0 license       |
| [Owlready2](https://bitbucket.org/jibalamy/owlready2/src/master/)      | LGPLv3+       |
| [Flask](https://pypi.org/project/Flask/)   | [BSD-3-Clause License](https://flask.palletsprojects.com/en/2.2.x/license/)        |
| [svelte-spa-router](https://github.com/ItalyPaleAle/svelte-spa-router)   | MIT license        |
| [svelte-range-slider-pips](https://github.com/simeydotme/svelte-range-slider-pips)      | MPL-2.0 license (not affecting this package's licence)      |


<!---
## Notes regarding changes to core parts of the software (beyond custom code addons):

#### Advanced live compiling of changes to internal Svelte files
(navigate to _13_overall_prototype02/my_package/frontend/ in terminal)
```
npm run dev
```


--->








