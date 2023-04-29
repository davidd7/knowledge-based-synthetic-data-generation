<script>
	import { getContext } from 'svelte';
	let contextData = getContext('context');

	export let label = "";
	export let unitLabel = "";
	export let valueKey = "";		
</script>


<div>
	{label}
	<input type="number" bind:value={contextData[valueKey]}/>
	{unitLabel}
</div>


<style>
</style>












