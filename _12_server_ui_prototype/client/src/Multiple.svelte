
<script>
	import ForwardContext from "./ForwardContext.svelte";
	export let array = [];
	export let newElement = {};
	export let debug = false;
	
	function addElement() {
		array.push( JSON.parse(JSON.stringify(newElement)) );
		array = array;
	}
	
	function removeElement(index) {
		console.log(index);
		array.splice(index, 1);
		array = array;
	}
</script>



<div>
	{#each array as array_element, i (array_element)}
		<ForwardContext context={array[i]}>
			<div class={"card"}>
				<slot/>
				<button on:click={() => {removeElement(i)}}>Remove element</button>
			</div>
		</ForwardContext>
	{/each}
</div>

<button on:click={ addElement }>Add Element</button>


{#if debug == true}
	{JSON.stringify(array)}
{/if}


<style>
	.card {
		border:1px solid #1a1a1a;
		margin: 8px;
		padding: 16px;
	}
</style>




















