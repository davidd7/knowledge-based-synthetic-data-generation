<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";
	import {writable} from 'svelte/store';
	import { setContext } from 'svelte';

	// import EinfachesModul from "../forms/EinfachesModul.svelte"



	const imports = {
		// "EinfachesModul": () => import('../forms/EinfachesModul.svelte')
		"EinfachesModul": (a) => import(`../forms/${a}.svelte`)
	};

	
	console.log(`../forms/EinfachesModul.svelte`);



    
	// Export params so that url params are inserted into it
	export let params;
	let feedbackText = "";

	let generation_scheme_data = { "name..." : "Loading"};

	let Thing;
	let store = writable('store');
	$store = {};
	setContext('context', store)


	let defaultData = ` {
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

	function handleSendButtonClick() {
		sendData();
	}





    onMount(async () => {
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

		generation_scheme_data = response_data;

		console.log(response_data)

		$store = JSON.parse(response_data.data);

		// Thing = (await import(`../forms/Einfaches-Modul.svelte`)).default;
		console.log(`../forms/${response_data.module_name}.svelte`);
		console.log(`../forms/EinfachesModul.svelte`);
		// Thing = (await import(`../forms/${response_data.module_name}.svelte`)).default;
		// console.log(await imports[response_data.module_name]());
		// Thing = (await imports[response_data.module_name]()).default;
		Thing = (await imports[response_data.module_name](response_data.module_name)).default;
		// Thing = (await import(`../forms/Einfaches-Modul.svelte`)).default;
	});
    






    async function sendData() {
        feedbackText = "Wird gesendet...";
		try {
			const response=await fetch(`/generation-schemes/${params.id}`,{
				method: 'PUT',
				headers: {
					'Accept': 'application/json, text/plain, */*',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify($store)
			});
			if(!response.ok) {
				throw new Error('Something went wrong');
			}
			const response_data=await response.json();
			// Könnte hier noch vgl machen, dass alle werte passen, aber wär eh zu spät
			console.log(response_data.id);
			console.log("Data was saved");
			feedbackText="Eingaben wurden gespeichert.";
		} catch(error) {
			console.log("Fehler: " + error);
			feedbackText="Beim Senden ist ein Problem aufgetreten.";
		}
    }

	async function reset() {
		$store = JSON.parse(defaultData);
		await sendData();
		Thing = (await import(`../forms/EinfachesModul.svelte`)).default;
		// console.log(`generation-schemes/${params.id}/edit`);
		// push(`/generation-schemes/${params.id}/edit`);
	}
</script>
    

<div class="page-header">
    <h1 style="flex-grow: 1;">
		{generation_scheme_data.name} ({generation_scheme_data.module_name})
	</h1>
	<button on:click={reset}>Reset</button>
	<button on:click={handleSendButtonClick}>Speichern</button>
</div>

<svelte:component this={Thing} />

<button on:click={handleSendButtonClick} class="app-send-button">Speichern</button>

<span>
	{feedbackText}
</span>





<style>

.app-send-button {
	margin-top: 16px;
}

</style>









