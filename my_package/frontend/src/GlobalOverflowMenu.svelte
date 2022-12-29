<script>
	import { onMount } from 'svelte';

    let debugModeValue = false;
    $:

    onMount( loadValues );
    


	async function loadValues() {
        let response = await fetch(`/settings/debug-mode/`, {
            method: 'GET'
		});

		if (!response.ok) {
			console.log( "An error occured: " + error );
			throw new Error('Something went wrong');
		}

		let response_data = await response.json();
        console.log(response_data);

		debugModeValue = response_data["value"];
	}


	async function updateValues() {
        let response = await fetch(`/settings/debug-mode/`, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"value":debugModeValue})
		});

		if (!response.ok) {
			console.log( "An error occured: " + error );
			throw new Error('Something went wrong');
		}

		let response_data = await response.json();

		debugModeValue = response_data["value"];
	}




</script>


Debug modes: <input type="checkbox" bind:checked={debugModeValue} on:change={updateValues} >