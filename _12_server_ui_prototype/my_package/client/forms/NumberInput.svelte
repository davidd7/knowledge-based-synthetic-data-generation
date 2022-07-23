
<script>
	export let label = "";
	export let unitLabel = "";
	
	export let data = [];
	export let valueKey = "";
	
	
/*	$: {
		data[valueKey] = data[valueKey];
	}*/
	
	
	
</script>





<div class={"number-input-container"}>
	{label}
	<input type="number" bind:value={data[valueKey]}/>
	{unitLabel}
	
</div>



<style>
	.number-input-container {
		
	}
</style>












