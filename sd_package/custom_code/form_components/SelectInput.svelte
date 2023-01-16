<script>
	export let label = "";
	
	export let data = [];
	export let valueKey = "";
	
	export let options = [];

/*	$: {
		data[valueKey] = data[valueKey];
	}*/
	
</script>


<div>
	{label}

	<select bind:value={data[valueKey]}>
		{#each options as option}
			<option  value={option.value}>
				{option.text}
			</option>
		{/each}
	</select>

</div>


<style>

</style>












