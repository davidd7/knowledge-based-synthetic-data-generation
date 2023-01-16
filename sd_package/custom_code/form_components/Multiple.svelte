
<script>
	import ForwardContext from "./ForwardContext.svelte";
	import { slide, fade } from 'svelte/transition';
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
			<div class={"element-container"}  transition:slide|local>
				<div class={"card"} transition:fade|local>
					<div style="font-weight: bold; padding-bottom: 6px;">Objekt {i + 1}</div>
					<slot/>
				</div>
				<button on:click={() => {removeElement(i)}} class="button-remove" transition:fade|local>x</button>
			</div>
		</ForwardContext>
	{/each}
</div>

<button on:click={ addElement }>Add object</button>


{#if debug == true}
	{JSON.stringify(array)}
{/if}


<style>
	.element-container {
		margin-bottom: 12px;
		display: flex;
		flex-direction: row;
	}
	.card {
		border:1px solid lightgrey;
		border-radius: 8px;
		padding: 16px;
		flex-grow: 1;
	}
	.button-remove {
		flex-grow: 0;
		width:40px;
		height: 40px;
		margin-left:8px;
		border-radius: 8px;
		padding: 0px;
	}
</style>




















