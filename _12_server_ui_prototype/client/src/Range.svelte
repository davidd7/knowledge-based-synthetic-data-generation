
<script>
	import { getContext } from 'svelte';
	let context_data = getContext('context');
	export let debug = false;

	import RangeSlider from "svelte-range-slider-pips";

	let data = context_data;

	export let rangeStartKey = 0; //data["minKey"];
	export let rangeEndKey = 0; //data["minKey"];
	export let minValue = 0; //data["minKey"];
	export let maxValue = 0; //data["minKey"];

	let test = [data[rangeStartKey],data[rangeEndKey]]

	$: {
		data[rangeStartKey] = test[0];
		//console.log("---");
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



