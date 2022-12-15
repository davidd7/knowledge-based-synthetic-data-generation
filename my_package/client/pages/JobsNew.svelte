<script>
	import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";

    let selected;
    let params = "{\n     \n}";


    let sdgeneneration_schemes = [];

    onMount(async () => {
        fetch('/generation-schemes', {
            method: 'GET'
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			sdgeneneration_schemes = response_data;
            
		}).catch( (error) => {
			console.log( "An error occurred: " + error );
		} );
	});
    
		
    function handleSubmit(event) {
        var formData = new FormData(event.currentTarget);

		fetch('/jobs', {
            method: 'POST',
            body: formData
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
            console.log(response_data.id);
            push(`/jobs`);
		}).catch( (error) => {
			// An error occured
			console.log( "An error occurred: " + error );
		} );

    }


</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">New generation job</h1> 
</div>



<form on:submit|preventDefault={handleSubmit} >

    <label for="generation_scheme">Base knowledge base:</label>
    <select bind:value={selected} id="knowledge_base_id" name="knowledge_base_id">
        {#each sdgeneneration_schemes as sdgeneneration_scheme}
            <option value={sdgeneneration_scheme.id}>
                {sdgeneneration_scheme.name}
            </option>
        {/each}
    </select>

    <p>

    <textarea bind:value={params} name="params" class="params-text-area"></textarea>

    <p>

    <button disabled={!selected} type=submit>
        Start
    </button>

</form>




<style>
.params-text-area {
    width: 100%;
    min-height: 150px;
}
</style>





















