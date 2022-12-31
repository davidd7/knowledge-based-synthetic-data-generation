
<script>
	import { getContext } from 'svelte';
	let context_data = getContext('context');
	console.log("Range.svelte received context: " );
	console.log(context_data);
	export let debug = false;

	import RangeSlider from "svelte-range-slider-pips";

	let data = context_data;

	export let rangeStartKey = 0;
	export let rangeEndKey = 0;
	export let minValue = 0;
	export let maxValue = 0;

	let test = [data[rangeStartKey],data[rangeEndKey]]

	$: {
		data[rangeStartKey] = test[0];
	}
	$: {
		data[rangeEndKey] = test[1];
	}


</script>


<div id="slider2">
	<RangeSlider min={minValue} max={maxValue}  bind:values={test} springValues={ {"stiffness":1, "damping":1 } } range pips all='label' />
</div>
{#if debug == true}
	{JSON.stringify(data)}
	{rangeStartKey}
	{data[rangeStartKey]}
	{data["min"]}
{/if}


<style>
	#slider2 {
		--matse-color: rgb(0,127,194);
		--slider-color: var(--matse-color);
		--range-handle-inactive: var(--slider-color); /* inactive handle color */
		--range-handle:          var(--slider-color); /* non-focussed handle color */
		--range-handle-focus:    var(--slider-color); /* focussed handle color */
	}
	
</style>



