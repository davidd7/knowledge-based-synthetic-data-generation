<script>
</script>
    

<div class="page-header">
    <h1 style="flex-grow: 1;">Configuration</h1> 
</div>


<div class="page-header">
    <h3 style="flex-grow: 1;">Overview</h3> 
</div>

<ul style="">
    <li>To add functionalities, open the directory of this application, navigate to the sd_package/custom_code/ subfolder and then edit the respective specific files (as outlined below).
    <li>To make the changes visible in the application, you have to restart the server or open the three-dot menu on the top right and click on the "Reload custom code" button.
</ul>


<div class="page-header">
    <h3 style="flex-grow: 1;">Modules</h3> 
</div>

<ul style="color: grey;">
    <li>By creating modules, new forms are available in the Knowledge Elicitation.
    <li>Modules are saved at sd_package/custom_code/modules/
    <li>Each module is a subfolder in that folder. You can create new modules by creating new folders there. The name of the folder will be the name of the module.
    <li>Each module folder contains up to 4 files that specify different parts of its behaviour
    <ul>
        <li>Form.svelte (required): Defines a form by combining and nesting form elements (see below).
        <li>__init__.py (required): Defines the generation algorithm. Gets as input the values entered into the form and sent via the API. Creates objects of different classes to specify the generation algorithm.
        <li>default.json (required): The form always exactly displays the values saved in a JSON object. When a new form is loaded, the values from this file are loaded into it.
        <li>defaultdata_mlsystem.json (optional): Specifies default values for the API. This can help understand what values your function accepts, and these values can be loaded when starting the generation process via the API to simplify things.
    </ul>
    <li>It is most easy to understand how modules work by copying one of our example modules and adapting it for your new task.
</ul>


<div class="page-header">
    <h3 style="flex-grow: 1;">Form components</h3> 
</div>

<ul style="color: grey;">
    <li>Form components are single svelte files that define single form elements.
    <li>Saved at sd_package/custom_code/form_components
    <li>These elements can then be used to create the Form.svelte files for the modules
</ul>




<div class="page-header">
    <h3 style="flex-grow: 1;">Ontology Layer</h3> 
</div>


<ul style="color: grey;">
    <li>The ontology layer contains reusable rendering functionality.
    <li>Saved at sd_package/custom_code/generation_components
    <li>There are two types of files here:
        <ul>
            <li>main.owl: This file defines an ontology (=classes and attriutes that can be used to describe generation algorithms). It can for example be edited with Protege.
            <li>Python files: These files contain handler objects that search through objects created in the modules generation algorithm. The onto_to_sd file registers all handlers that should be used for the generation process.
        </ul>
</ul>








