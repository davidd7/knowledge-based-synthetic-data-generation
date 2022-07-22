


<script>
	import { getContext } from 'svelte';
	let context_data = getContext('context');
	
	let data = context_data;
	export let valueKey = 0;
	
	console.log("Input3DModel initializes");
	console.log(data);
	console.log(valueKey);
	// $: hintText = (data[valueKey] == "") ? "rrr" : hintText = data[valueKey];
	// let hintText = (data[valueKey] == "") ? "rrr" : hintText = data[valueKey];
	$: {
		// data[valueKey] = hintText;
		data[valueKey] = data[valueKey]
	}
	
	let inputFile;
	let inputText;
	// console.log(inputFile);
	// $: if (inputFile != undefined) {
	// 	console.log(inputFile);
	// 	/*inputFile.onchange = () => {
	// 		console.log("==> YEAH")
	// 		console.log(inputFile.value);
	// 	}*/
	// }
	
	function fileChanged() {
			var formData = new FormData()
			formData.append('file', inputFile.files[0])

			inputText.value = "";
			inputText.placeholder = "Lädt...";
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

				console.log("Received answer!");
				console.log(response_data);
				//inputText.value = data;
				//hintText = data;
				data[valueKey] = response_data;
				inputText.placeholder = "Keine Datei hochgeladen";
			}).catch( (error) => {
				inputText.placeholder = "Fehler: " + error;
			} );


	}
	

</script>




<input bind:this={inputText} type="text" disabled="true" placeholder="Keine Datei hochgeladen" value={data[valueKey]} />

<button>Datei auswählen</button>

<input bind:this={inputFile} type="file" label="asdsad" on:change={fileChanged} />










<style>
</style>








