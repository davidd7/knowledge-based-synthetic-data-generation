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


	async function sendReloadCustomCode() {
		let response = await fetch(`/settings/reload-custom-code`, { method: 'POST' } );

		console.log(response);

		if (!response.ok) {
			// Error
			console.log("Error occurred during abort call");
			return;
		}

		if (response.ok) {
			if (confirm("Custom code reloaded. Reload webpage?") == true) {
				window.location.reload();
			} else {
				// Do nothing
			}
		}

		// loadData()
	}




</script>


<span style="white-space:nowrap;">Debug mode: <input type="checkbox" bind:checked={debugModeValue} on:change={updateValues} ></span>
<span style="white-space:nowrap;">Reload custom code:
	<button on:click={sendReloadCustomCode} class="table-button">
		<img src="pics/refresh_FILL1_wght400_GRAD0_opsz48.svg" class="table-button-icon" alt="delete"/>
	</button>
</span>



