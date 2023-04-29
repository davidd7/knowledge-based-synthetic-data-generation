
## Autonomous and Knowledge-based Synthetic Data Generation

This software adds an autonomy layer and an abstraction layer on top of BlenderProc.

With the autonomy layer...
* Programmers can program modules that define a form and API for a synthetic data generation pipeline
* Process Experts can influence the generation process via a web-based UI
* Other systems can trigger trigger synthetic data generation via a REST API

With the abstraction layer...
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
flask --app sd_package --debug init-db
```

#### 6) Install packages needed for frontend

* Navigate to ...\sd_package\frontend\
* ```npm install```

## Starting the server

### Option 1: Start Flask server in production mode (recommended)

* Several WSGI servers are available for Flask applications ([list](https://flask.palletsprojects.com/en/2.2.x/deploying/))
* In the following, the steps when using the WSGI server "[waitress](https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/)" are shown:

#### 1) Start virtual environment (venv) (if not still active)

* Navigate to ...\knowledge-based-synthetic-data-generation\
* Execute the following commands:

```
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```

#### 2) Install waitress in the virtual environment (venv)

```
pip install waitress
```

#### 3) Start the server

```
waitress-serve --port=8080 --call 'sd_package:create_app'
```

#### 4) Open the web application in a browser

* Open the server's ip address in a browser to access the web application
* For instance, if the server and browser are on the same computer, type [`http://localhost:8080/`](http://localhost:8080/) or [`http://127.0.0.1:8080/`](http://127.0.0.1:8080/) into the URL bar

---

### Option 2: Start Flask server in debug mode (**not** recommended)

* PLEASE NOTE: Running in debug note is not recommended even for small deployments. For instance, 3d model uploads are unreliable and often don't work on the debug server. Instead, please use a production server (see above).

#### 1) Start virtual environment (venv) (if not still active)

* Navigate to ...\knowledge-based-synthetic-data-generation\
* Execute the following commands:

```
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```

#### 2) Start the flask server

```
flask --app sd_package --debug run
```

* (--debug can be left away if changes in flask source code should not automatically be compiled)

#### 3) Open the web application in a browser

* When starting the server, it's IP address will be printed. Copy this address into a browser's url bar to access the web application
* For instance, if the server and browser are on the same computer, type [`http://localhost:5000/`](http://localhost:500/) or [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/) into the URL bar

## Used software

| Software    | Licence     | Citation     |
| ----------- | ----------- | ------------ |
| [BlenderProc](https://github.com/DLR-RM/BlenderProc)      | GPL-3.0 license       | M. Denninger, M. Sundermeyer, D. Winkelbauer, Y. Zidan, D. Olefir, M. Elbadrawy, A. Lodhi, and H. Katam, “Blenderproc,” 2019. |
| [Owlready2](https://bitbucket.org/jibalamy/owlready2/src/master/)      | LGPLv3+ licence       | J.-B. Lamy, “Owlready: Ontology-oriented programming in python with automatic classification and high level constructs for biomedical ontologies,” Artificial Intelligence in Medicine, vol. 80, pp. 11–28, 2017. |
| [Flask](https://pypi.org/project/Flask/)   | BSD 3-clause license        | - |
| [svelte-spa-router](https://github.com/ItalyPaleAle/svelte-spa-router)   | MIT license        | - |
| [svelte-range-slider-pips](https://github.com/simeydotme/svelte-range-slider-pips)      | MPL-2.0 license (not affecting this package's licence)      | - |



<!---
## Notes regarding changes to core parts of the software (beyond custom code addons):

#### Advanced live compiling of changes to internal Svelte files
(navigate to _13_overall_prototype02/sd_package/frontend/ in terminal)
```
npm run dev
```
--->








