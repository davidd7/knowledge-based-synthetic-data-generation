<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
    import { params, push } from "svelte-spa-router";

	//export let params = {};

    // let selected;
    // let name;

    let sdgeneneration_modules = [];

    onMount(async () => {

        fetch('/modules', {
            method: 'GET'
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			if (response_data == "") {
				throw new Error('Something went wrong');
			}
            console.log(response_data);
			sdgeneneration_modules = response_data;
			// inputText.placeholder = "Keine Datei hochgeladen";
		}).catch( (error) => {
			// nputText.placeholder = "Fehler: " + error;
		} );




		// const res = await fetch(`/tutorial/api/album`);
		// photos = await res.json();
	});
    
		
    function handleSubmit(event) {
        
        var formData = new FormData(event.currentTarget); //new FormData()
        console.log(test)
		//formData.append('file', inputFile.files[0]);
        

		// inputText.value = "";
		// inputText.placeholder = "Lädt...";

		fetch('/generation-schemes', {
            method: 'POST',
            body: formData
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			// if (response_data == "") {
			// 	throw new Error('Something went wrong');
			// }
			// data[valueKey] = response_data;
			// inputText.placeholder = "Keine Datei hochgeladen";
            console.log(response_data.id); // TODO: Hier muss mit JS/SPA auf richtige Seite weiterleiten !
            push(`/generation-scheme/${response_data.id}/edit`);
		}).catch( (error) => {
			console.log( "Fehler: " + error );
		} )


    }

let test;

</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">TEST EDIT {params.id}</h1> 
</div>



<!-- <form on:submit|preventDefault={handleSubmit} bind:this={test}>

    <label for="name">Name:</label>
    <input bind:value={name} id="name" name="name" />

    <label for="modul_name">Modul:</label>
    <select value={selected} on:change="{() => name = ''}" id="modul_name" name="module_name">
        {#each sdgeneneration_modules as sdgeneneration_module}
            <option value={sdgeneneration_module.name}>
                {sdgeneneration_module.name}
            </option>
        {/each}
    </select>


    <button disabled={!name} type=submit>
        Erstellen
    </button>

</form> -->









<!-- {#each sdgeneneration_modules as el}
    <div>
        {el.name}, {el.module_name} <button>Edit</button>
    </div>
{/each} -->






















