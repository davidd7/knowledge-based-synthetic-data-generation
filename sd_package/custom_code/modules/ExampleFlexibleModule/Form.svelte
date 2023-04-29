<script>
	// Import general components
	import { getContext, setContext } from 'svelte';
	// Import form components
	import DynamicList from '../form_components/DynamicList.svelte';
	import RangeInput from '../form_components/RangeInput.svelte';
	import HeadlinedGroup from '../form_components/HeadlinedGroup.svelte';
	import NumberInput from '../form_components/NumberInput.svelte';
	import Upload3DModelInput from '../form_components/Upload3DModelInput.svelte';

	// Set up reactivity (must be in all form files)
	let data;
	$: { data = data; }
	let store = getContext('context');
	store.subscribe(value => { data = value; });
	setContext('context', data);
</script>



<div class="app-container">
	<HeadlinedGroup headline="Objects to recognize">
		<DynamicList array={data.objects_to_recognize} newElement={ {url:"", min:3, max:6} }>
			3D model:
			<Upload3DModelInput valueKey={"url"} />
			<p>
			How many instances of this object type should appear per image:
			<RangeInput minValue={0} maxValue={10} rangeStartKey={"min"} rangeEndKey={"max"} />
		</DynamicList>
	</HeadlinedGroup>
	<HeadlinedGroup headline="Area, in which all objects appear">
		<NumberInput label="Length in the X direction:" unitLabel="mm" valueKey={"area_length_x"} />
		<NumberInput label="Length in the Y direction:" unitLabel="mm" valueKey={"area_length_y"} />
	</HeadlinedGroup>
	<HeadlinedGroup headline="Camera">
		<NumberInput label="Height above table:" unitLabel="mm" valueKey={"camera_height"} />
	</HeadlinedGroup>
</div>





