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
	<HeadlinedGroup headline="Objects to recognize">
		<Multiple array={data.objects_to_recognize} newElement={ {url:"", min:3, max:6} }>
			3D model:
			<Input3DModel valueKey={"url"} />
			<p>
			How many instances of this object type should appear per image:
			<Range minValue={0} maxValue={10} rangeStartKey={"min"} rangeEndKey={"max"} />
		</Multiple>
	</HeadlinedGroup>
	<HeadlinedGroup headline="Area, in which all objects appear">
		<NumberInput label="Length in the X direction:" unitLabel="mm"  data={data} valueKey={"area_length_x"} />
		<NumberInput label="Length in the Y direction:" unitLabel="mm"  data={data} valueKey={"area_length_y"} />
	</HeadlinedGroup>
	<HeadlinedGroup headline="Camera">
		<NumberInput label="Height above table:" unitLabel="mm"  data={data} valueKey={"camera_height"} />
	</HeadlinedGroup>
</div>





