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
	<HeadlinedGroup headline="Possible number of objects per image">
		Objects of class 1 (=gear with few big teeth):
		<HeadlinedGroup headline="">
			<Range minValue={0} maxValue={20} rangeStartKey={"class1_min"} rangeEndKey={"class1_max"} />
		</HeadlinedGroup>
		<div style="height: 16px;"/>
		<!-- <p> -->
		Objects of class 2 (=gear with many small teeth):
		<HeadlinedGroup headline="">
			<Range minValue={0} maxValue={20} rangeStartKey={"class2_min"} rangeEndKey={"class2_max"} />
		</HeadlinedGroup>
	</HeadlinedGroup>
	<div style="height: 1px;"/>
	<HeadlinedGroup headline="Area, in which all objects appear">
		<SelectInput label="" data={data} valueKey={"location"} options={[{value:"full", text:"full"}, {value:"half_left", text:"left half only"}, {value:"half_right", text:"right half only"}]} />
	</HeadlinedGroup>
</div>





