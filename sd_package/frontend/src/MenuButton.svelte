<script>
	let active = false;
	function toggleMenu() {	active = !active;	}
</script>

<div class="container">
	<img src="pics/more_vert_black_24dp.svg"  on:click={toggleMenu} class="button" alt="more settings"/>
	<!-- <button on:click={toggleMenu} class="button">Menu</button> -->
	<div class="dropdown-container">
		{#if active}
			<div class="dropdown">
				<slot></slot>
			</div>
		{/if}
	</div>
</div>

<style>
	.container {
		text-align: right;
	}
	
	.button {
		position: relative;
		margin-bottom: 0px;
	}
	
	.dropdown {
		position: absolute;
		top: 100%;
		right: 0;
		background: white;
		border: 1px solid black;
		padding: .3rem;
		z-index: 5;
	}
	
	.dropdown-container {
		 position: relative;
	}
</style>