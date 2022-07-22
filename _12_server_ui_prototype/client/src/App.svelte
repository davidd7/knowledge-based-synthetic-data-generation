<script>
import Multiple from './Multiple.svelte';
import Range from './Range.svelte';
import HeadlinedGroup from './HeadlinedGroup.svelte';
import NumberInput from './NumberInput.svelte';
import Input3DModel from './Input3DModel.svelte';

import {writable} from 'svelte/store';
let store = writable('store');
	
let data = JSON.parse(`
							{
									"objects_to_recognize": [
											{
											"url": "media/untitled.obj",
											"min": 2,
											"max": 5
											},
											{
											"url": "media/untitled.obj",
											"min": 3,
											"max": 6
											},
											{
											"url": "",
											"min": 3,
											"max": 3
											}
									],
									"area_length_x": 3,
									"area_length_y": 7,
									"camera_height": 5
							}`);
	
	$store = data;
	
	function test() {
		alert(JSON.stringify($store));
	}
	
</script>


<HeadlinedGroup headline="Objekte, die erkannt werden sollen:">
	<Multiple array={$store.objects_to_recognize} newElement={ {url:"", min:3, max:6} }>
		3D-Modell:
		<Input3DModel valueKey={"url"} />
		<p>
		Wieviele Objekte dieses Typs pro Bild:
		<Range minValue={0} maxValue={10} rangeStartKey={"min"} rangeEndKey={"max"} />
	</Multiple>
</HeadlinedGroup>
<HeadlinedGroup headline="Szene modellieren:">
	<HeadlinedGroup headline="Bereich, in dem alle Objekte erscheinen:">
		<NumberInput label="Länge in x-Richtung:" unitLabel="mm"  data={$store} valueKey={"area_length_x"} />
		<NumberInput label="Länge in y-Richtung:" unitLabel="mm"  data={$store} valueKey={"area_length_y"} />
	</HeadlinedGroup>
	<HeadlinedGroup headline="Kamera:">
		<NumberInput label="Höhe über Tisch:" unitLabel="mm"  data={$store} valueKey={"camera_height"} />
	</HeadlinedGroup>
</HeadlinedGroup>
<button on:click={test}>Absenden</button>












