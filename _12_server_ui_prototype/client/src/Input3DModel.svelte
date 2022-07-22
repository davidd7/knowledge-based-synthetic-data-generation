


<script>
	import { getContext } from 'svelte';
	let context_data = getContext('context');
	
	let data = context_data;
	export let valueKey = 0;
	
	console.log(data);
	console.log(valueKey);
	$: hintText = (data[valueKey] == "") ? "rrr" : hintText = data[valueKey];
	
	
	let inputFile;
	console.log(inputFile);
	$: if (inputFile != undefined) {
		console.log(inputFile);
		/*inputFile.onchange = () => {
			console.log("==> YEAH")
			console.log(inputFile.value);
		}*/
	}
	
	function fileChanged() {
			console.log("==> YEAH")
			console.log(inputFile.value);
	}
	
</script>




<input id="inputText" type="text" disabled="true" placeholder="Keine Datei hochgeladen" value={hintText} />

<button>Datei auswählen</button>

<input bind:this={inputFile} type="file" label="asdsad" on:change={fileChanged} />










<style>
</style>








