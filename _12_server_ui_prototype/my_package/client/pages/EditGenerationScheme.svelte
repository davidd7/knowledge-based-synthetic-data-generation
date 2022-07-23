<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";
    
	export let params;
	let generation_scheme_data = { "name..." : "Loading"};



	let Thing;






	import {writable} from 'svelte/store';
	let store = writable('store');
		


	let template_data = ` {
		"objects_to_recognize": [
			{
				"url": "media/untitled.obj",
				"min": 2,
				"max": 5
			},
			{
				"url": "media/untitled.obj",
				"min": 3,
				"max": 6
			},
			{
				"url": "",
				"min": 3,
				"max": 3
			}
		],
			"area_length_x": 3,
			"area_length_y": 7,
			"camera_height": 5
	}`;



	let data = JSON.parse(` {
		"objects_to_recognize": [
			{
				"url": "media/untitled.obj",
				"min": 2,
				"max": 5
			},
			{
				"url": "media/untitled.obj",
				"min": 3,
				"max": 6
			},
			{
				"url": "",
				"min": 3,
				"max": 3
			}
		],
			"area_length_x": 3,
			"area_length_y": 7,
			"camera_height": 5
	}`);
	
	$store = data;
	

	

	import { setContext } from 'svelte';
	//export let context = {};
	setContext('context', store)



	function test() {
		// alert(JSON.stringify($store));
		handleSubmit();
	}



















    onMount(async () => { //

		console.log(params);

        let response = await fetch(`/generation-schemes/${params.id}`, {
            method: 'GET'
		}).catch( (error) => {
			console.log( "An error occured: " + error );
		} );

		if (!response.ok) {
			console.log( "An error occured: " + error );
			throw new Error('Something went wrong');
		}

		let response_data = await response.json();

		console.log(response_data);
		generation_scheme_data = response_data;


		data = JSON.parse(response_data.data);
		$store = data;


		// Thing = (await import(`../forms/${generation_scheme_data.module_name}.svelte`)).default;
		Thing = (await import(`../forms/Einfaches-Modul.svelte`)).default;




	});
    
		











    function handleSubmit() {
        
		fetch(`/generation-schemes/${params.id}`, {
            method: 'PUT',
			headers: {
			'Accept': 'application/json, text/plain, */*',
			'Content-Type': 'application/json'
			},
    		body: JSON.stringify($store)
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			// KÖnnte hier noch vgl machen, dass alle werte passen, aber wär eh zu spät

            console.log(response_data.id); // TODO: Hier muss mit JS/SPA auf richtige Seite weiterleiten !
            // push(`/generation-scheme/${response_data.id}/edit`);
			console.log("Data was saved")
		}).catch( (error) => {
			console.log( "Fehler: " + error );
		} )


    }




function reset() {
	$store = JSON.parse(template_data);
	console.log($store);
	handleSubmit();
}



</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">{generation_scheme_data.name} ({generation_scheme_data.module_name})</h1> <button on:click={reset}>reset</button>
</div>






<svelte:component this={Thing} >
  <p>some slotted content</p>
</svelte:component>


<button on:click={test} class="app-send-button">Absenden</button>


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






















