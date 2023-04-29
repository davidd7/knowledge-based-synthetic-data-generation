<script>
	import { getContext } from 'svelte';
	let contextData = getContext('context');

	export let label = "";
	export let valueKey = "";
	export let options = [];	
</script>


<div>
	{label}

	<select bind:value={contextData[valueKey]}>
		{#each options as option}
			<option  value={option.value}>
				{option.text}
			</option>
		{/each}
	</select>

</div>


<style>

</style>












