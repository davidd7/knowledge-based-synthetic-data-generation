<script>
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { setContext } from 'svelte';

	// Export params so that url params are inserted into it
	export let params;
	export let globalProps;

	let feedbackText = "";

	let generation_scheme_data = { "name..." : "Loading"};

	let Thing;
	let store = writable('store');
	$store = {};

	setContext('context', store);
	let kb_name = "loading...";

	let originalData = "";


	function handleSendButtonClick() {
		sendData();
	}


	function customHasUnsavedDataCheck() {
		return JSON.stringify( { name : kb_name, data : $store }) != originalData;
	}


    onMount( () => {
		overrideCurrentDataWithDataFromServer();
		// Connect our customHasUnsavedDataCheck function to globalProps
		globalProps.hasUnsavedData = customHasUnsavedDataCheck;
	} );


	async function overrideCurrentDataWithDataFromServer() {
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
		kb_name = generation_scheme_data.name;
		$store = JSON.parse(response_data.data);
		originalData = JSON.stringify( { name : kb_name, data : $store });
		Thing = undefined;
		Thing = (   await import(`../forms/${response_data.module_name}.svelte`)  ).default;
	}




    async function sendData() {
		console.log("Sending to server:");
		console.log(JSON.stringify($store));
        feedbackText = "Sending...";
		try {
			const response = await fetch(`/generation-schemes/${params.id}`,{
				method: 'PUT',
				headers: {
					'Accept': 'application/json, text/plain, */*',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify( { name : kb_name, data : $store })
			});
			if(!response.ok) {
				throw new Error('Something went wrong');
			}
			const response_data = await response.json();
			console.log(response_data);
			originalData = JSON.stringify( { name : kb_name, data : $store });

			feedbackText = "Input was saved.";
		} catch(error) {
			console.log("Error: " + error);
			feedbackText = "An error occurred while sending the data.";
		}
    }

	async function reset() {
		console.log("Reset clicked");
		overrideCurrentDataWithDataFromServer();
	}
	
</script>
    

<div class="page-header">
	<input style="flex-grow: 1;" bind:value={kb_name} type="text" class={'input-knowledge-base-name'}>
	<button on:click={reset} class={'edit-scheme-button'}>Reset</button>
	<button on:click={handleSendButtonClick} class={'edit-scheme-button'}>Save</button>
</div>

<svelte:component this={Thing} />

<button on:click={handleSendButtonClick} class="app-send-button">Save</button>

<span>
	{feedbackText}
</span>





<style>

.app-send-button {
	margin-top: 16px;
}

.edit-scheme-button {
	margin-top: 9px;
}

.input-knowledge-base-name {
	border: 0px solid black;
	font-size: 2rem;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
	font-weight: bold;
	padding: 8px;
	margin-block-start: 0.67em;
    margin-block-end: 0.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
	padding-left: 0px;
}

</style>









