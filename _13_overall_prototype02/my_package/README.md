# Starting the Flask server for the first time
(navigate to _13_overall_prototype02/ in terminal)
py -3 -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
pip install Flask
$env:FLASK_APP = "my_package"
$env:FLASK_ENV = "development"
flask init-db
flask run


pip install Owlready2


# Starting the Flask server
(navigate to _13_overall_prototype02/ in terminal)
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
$env:FLASK_APP = "my_package"
$env:FLASK_ENV = "development"
flask run

# Making changes to the Svelte files
(navigate to _13_overall_prototype02/my_package/client/ in terminal)
npm run dev

# Todo: Using Svelte for the first time
(navigate to _13_overall_prototype02/my_package/client/ in terminal)
npm install







