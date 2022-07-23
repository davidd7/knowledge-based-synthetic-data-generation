<script>
	import Multiple from './Multiple.svelte';
	import Range from './Range.svelte';
	import HeadlinedGroup from './HeadlinedGroup.svelte';
	import NumberInput from './NumberInput.svelte';
	import Input3DModel from './Input3DModel.svelte';


	import { getContext } from 'svelte';

	let data = {};

	let store = getContext('context');
	store.subscribe(value => {
		console.log(value);
		data = value;
		console.log(data);
		// data = data;
	})


// $: 	console.log(store);



	// import {writable} from 'svelte/store';
	// let store = writable('store');
		
	// let data = JSON.parse(` {
	// 	"objects_to_recognize": [
	// 		{
	// 			"url": "media/untitled.obj",
	// 			"min": 2,
	// 			"max": 5
	// 		},
	// 		{
	// 			"url": "media/untitled.obj",
	// 			"min": 3,
	// 			"max": 6
	// 		},
	// 		{
	// 			"url": "",
	// 			"min": 3,
	// 			"max": 3
	// 		}
	// 	],
	// 		"area_length_x": 3,
	// 		"area_length_y": 7,
	// 		"camera_height": 5
	// }`);
	
	// $store = data;
	
	// function test() {
	// 	alert(JSON.stringify($store));
	// }
	
</script>


<div class="app-container">
	<!-- {JSON.stringify(data)} -->
	<HeadlinedGroup headline="Zu erkennende Objekte">
		<Multiple array={data.objects_to_recognize} newElement={ {url:"", min:3, max:6} }>
			3D-Modell:
			<Input3DModel valueKey={"url"} />
			<p>
			Wieviele Objekte dieses Typs pro Bild:
			<Range minValue={0} maxValue={10} rangeStartKey={"min"} rangeEndKey={"max"} />
		</Multiple>
	</HeadlinedGroup>
	<HeadlinedGroup headline="Bereich, in dem alle Objekte erscheinen">
		<NumberInput label="Länge in x-Richtung:" unitLabel="mm"  data={data} valueKey={"area_length_x"} />
		<NumberInput label="Länge in y-Richtung:" unitLabel="mm"  data={data} valueKey={"area_length_y"} />
	</HeadlinedGroup>
	<HeadlinedGroup headline="Kamera">
		<NumberInput label="Höhe über Tisch:" unitLabel="mm"  data={data} valueKey={"camera_height"} />
	</HeadlinedGroup>
	<!-- <button on:click={test} class="app-send-button">Absenden</button> -->
</div>



<style>
	.app-container {
		max-width: 1000px;
		margin-left: auto;
		margin-right: auto;
		padding-bottom: 60px;
	}
	/* .app-send-button {
		margin-top: 16px;
	} */
</style>



