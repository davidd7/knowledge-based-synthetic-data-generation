<script>
	import { getContext } from 'svelte';
	let contextData = getContext('context');
	
	let data = contextData;
	export let valueKey = 0;
	
	console.log("3DModelInput initializes");
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

		try {

			let response = await fetch('/files', {
				method: 'POST',
				body: formData
			});
			
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			let response_data = await response.text();

			if (response_data == "") {
				throw new Error('Something went wrong');
			}
			
			data[valueKey] = response_data;
			inputText.placeholder = "No file uploaded";
			inputFile.value = "";
			console.log("Upload was successful")

		} catch (error) {
			inputText.placeholder = "Error. Please try again.";
			inputFile.value = "";
            console.log("Error during file upload. If you are running flask on the dev server, use a production server instead for successfull file uploads.");
			await sleep(1000);
		}





	}
	


	function sleep(ms) {
    	return new Promise(resolve => setTimeout(resolve, ms));
	}


</script>




<input bind:this={inputText} type="text" disabled="true" placeholder="No file uploaded" value={data[valueKey]} />

<button on:click={()=>inputFile.click()}>Select file</button>

<div class={"input-file-container"}>
<input bind:this={inputFile} type="file" on:change={fileChanged} class={"input-file"} />
</div>









<style>
	.input-file-container {
		height: 0px;
		overflow: hidden;
		width: 0px;
	}
	.input-file {
		visibility: hidden;
	}
</style>








