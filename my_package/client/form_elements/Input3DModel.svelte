


<script>
	import { getContext } from 'svelte';
	let context_data = getContext('context');
	
	let data = context_data;
	export let valueKey = 0;
	
	console.log("Input3DModel initializes");
	console.log(data);
	console.log(valueKey);
	$: {
		data[valueKey] = data[valueKey]
	}
	
	let inputFile;
	let inputText;
	
	async function fileChanged() {
		// Prepare what to send
		var formData = new FormData()
		formData.append('file', inputFile.files[0]);

		inputText.value = "";
		inputText.placeholder = "Loading...";

		let success = false;
		let attempts = 0;

		while (!success && attempts < 1) {

			try {

				let response = await fetch('/files', {
					method: 'POST',
					body: formData
				});
				
				if (!response.ok) {
					throw new Error('Something went wrong');
					// inputText.placeholder = "Error: " + error;
				}
				let response_data = await response.text();

				if (response_data == "") {
					throw new Error('Something went wrong');
				}
				data[valueKey] = response_data;
				inputText.placeholder = "No file uploaded";
				success = true;
				console.log("Upload was successful")

			} catch (error) {
				inputText.placeholder = "Error: " + error;
				console.log("Attempt " + (attempts + 1) + " of 1 unsuccessful.");
				console.log("If you are running flask on the dev server, use a production server instead for successfull file uploads.");
				attempts += 1;
				await sleep(1000);
			}

		}




	}
	


	function sleep(ms) {
    	return new Promise(resolve => setTimeout(resolve, ms));
	}


</script>




<input bind:this={inputText} type="text" disabled="true" placeholder="No file uploaded" value={data[valueKey]} />

<button on:click={()=>inputFile.click()}>Select file</button>

<input bind:this={inputFile} type="file" on:change={fileChanged}  class={"input-file"} />










<style>
	.input-file {
		visibility: hidden;
	}
</style>








