<script>
	// Import general components
	import { getContext, setContext } from 'svelte';
	// Import form elements
	import Multiple from '../form_components/Multiple.svelte';
	import Range from '../form_components/Range.svelte';
	import HeadlinedGroup from '../form_components/HeadlinedGroup.svelte';
	import NumberInput from '../form_components/NumberInput.svelte';
	import Input3DModel from '../form_components/Input3DModel.svelte';
    import ForwardContext from '../form_components/ForwardContext.svelte';

	let data;
	$: { data = data; }

	let store = getContext('context');
	store.subscribe(value => {
		data = value;
	});
	setContext('context', data)

	console.log("(ExampleExperimentModule)Form.svelte received context: " );
	console.log(store);
	console.log("(ExampleExperimentModule)Form.svelte received context.subscribe: " );
	console.log(data);

</script>


<div class="app-container">
	<HeadlinedGroup headline="Objects to recognize">
		How many instances of class 1 should appear per image:
		<Range minValue={0} maxValue={40} rangeStartKey={"class1_min"} rangeEndKey={"class1_max"} />
		<p>
		How many instances of class 2 should appear per image:
		<Range minValue={0} maxValue={40} rangeStartKey={"class2_min"} rangeEndKey={"class2_max"} />
	</HeadlinedGroup>
	<HeadlinedGroup headline="Area, in which all objects appear">
		<NumberInput label="Length in the X direction:" unitLabel="mm"  data={data} valueKey={"area_length_x"} />
		<NumberInput label="Length in the Y direction:" unitLabel="mm"  data={data} valueKey={"area_length_y"} />
	</HeadlinedGroup>
	<HeadlinedGroup headline="Camera">
		<NumberInput label="Height above table:" unitLabel="mm"  data={data} valueKey={"camera_height"} />
	</HeadlinedGroup>
</div>





