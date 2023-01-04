<script>
	// Import general components
	import { getContext, setContext } from 'svelte';
	// Import form elements
	import Range from '../form_components/Range.svelte';
	import HeadlinedGroup from '../form_components/HeadlinedGroup.svelte';
	import NumberInput from '../form_components/NumberInput.svelte';
    import SelectInput from '../form_components/SelectInput.svelte';

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
		HHow many instances of class 1 should appear per image:
		<Range minValue={0} maxValue={40} rangeStartKey={"class1_min"} rangeEndKey={"class1_max"} />
		<p>
		How many instances of class 2 should appear per image:
		<Range minValue={0} maxValue={40} rangeStartKey={"class2_min"} rangeEndKey={"class2_max"} />
	</HeadlinedGroup>
	<p>
	<HeadlinedGroup headline="Area, in which all objects appear">
		<SelectInput label="" data={data} valueKey={"location"} options={[{value:"full", text:"full"}, {value:"half_left", text:"left half only"}, {value:"half_right", text:"right half only"}]} />
	</HeadlinedGroup>
</div>





