<script>
	import { onMount } from 'svelte';
	import {writable} from 'svelte/store';
	import { setContext } from 'svelte';

	// Export params so that url params are inserted into it
	export let params;

	let feedbackText = "";

	let generation_scheme_data = { "name..." : "Loading"};

	let Thing;
	let store = writable('store');
	$store = {};
	setContext('context', store);

	function handleSendButtonClick() {
		sendData();
	}



    onMount( overrideCurrentDataWithDataFromServer );
    


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

		generation_scheme_data = response_data;
		$store = JSON.parse(response_data.data);
		Thing = (   await import(`../forms/${response_data.module_name}.svelte`)  ).default;
	}




    async function sendData() {
		console.log("Sending to server:");
		console.log(JSON.stringify($store));
        feedbackText = "Sending...";
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
			// 
			console.log(response_data.id);
			console.log("Data was saved");
			feedbackText="Input was saved.";
		} catch(error) {
			console.log("Error: " + error);
			feedbackText="An error occurred while sending the data.";
		}
    }

	async function reset() {
		overrideCurrentDataWithDataFromServer();
	}
	
</script>
    

<div class="page-header">
    <h1 style="flex-grow: 1;">
		{generation_scheme_data.name} (base module: {generation_scheme_data.module_name})
	</h1>
	<button on:click={reset}>Reset</button>
	<button on:click={handleSendButtonClick}>Save</button>
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

</style>









