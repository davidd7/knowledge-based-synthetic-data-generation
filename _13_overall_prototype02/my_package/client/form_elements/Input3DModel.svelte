


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
	
	function fileChanged() {
		// Prepare what to send
		var formData = new FormData()
		formData.append('file', inputFile.files[0]);

		inputText.value = "";
		inputText.placeholder = "Loading...";

		fetch('/upload', {
			method: 'POST',
			body: formData
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.text();
		}).then(response_data => {
			if (response_data == "") {
				throw new Error('Something went wrong');
			}
			data[valueKey] = response_data;
			inputText.placeholder = "No file uploaded";
		}).catch( (error) => {
			inputText.placeholder = "Error: " + error;
		} );


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








