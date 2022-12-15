<script>
	import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";

    let selected;
    let name;

    let sdgeneneration_modules = [];

    onMount(async () => {
        fetch('/modules', {
            method: 'GET'
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			sdgeneneration_modules = response_data;
		}).catch( (error) => {
			// An error occured
			console.log( "An error occurred: " + error );
		} );
	});
    
		
    function handleSubmit(event) {
        var formData = new FormData(event.currentTarget);

		fetch('/generation-schemes', {
            method: 'POST',
            body: formData
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
            console.log(response_data.id);
            push(`/generation-schemes/${response_data.id}/edit`);
		}).catch( (error) => {
			// An error occured
			console.log( "An error occurred: " + error );
		} );

    }


</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">New scheme</h1> 
</div>



<form on:submit|preventDefault={handleSubmit} >

    <label for="name">Name:</label>
    <input bind:value={name} id="name" name="name" />

    <label for="modul_name">Module:</label>
    <select value={selected} on:change="{() => name = ''}" id="modul_name" name="module_name">
        {#each sdgeneneration_modules as sdgeneneration_module}
            <option value={sdgeneneration_module.name}>
                {sdgeneneration_module.name}
            </option>
        {/each}
    </select>


    <button disabled={!name} type=submit>
        Create
    </button>

</form>


























