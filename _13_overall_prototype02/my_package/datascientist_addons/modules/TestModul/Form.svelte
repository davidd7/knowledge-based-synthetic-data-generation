<script>
	// Import general components
	import { getContext } from 'svelte';
	// Import form elements
	import Multiple from '../form_elements/Multiple.svelte';
	import Range from '../form_elements/Range.svelte';
	import HeadlinedGroup from '../form_elements/HeadlinedGroup.svelte';
	import NumberInput from '../form_elements/NumberInput.svelte';
	import Input3DModel from '../form_elements/Input3DModel.svelte';

	let data;
	$: { data = data; }

	let store = getContext('context');
	store.subscribe(value => {
		data = value;
	})
</script>


<div class="app-container">
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
</div>





