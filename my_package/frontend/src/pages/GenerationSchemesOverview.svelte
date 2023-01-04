<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
    import Router, { link } from "svelte-spa-router";

    let datas = [];

    onMount(async () => {
		loadData();
	});


	async function loadData() {
        fetch('/generation-schemes', {
            method: 'GET'
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			// console.log("START?")
			// // if (response_data == "") {
			// // 	throw new Error('Something went wrong');
			// // }
            console.log(response_data);
			datas = response_data;
			// inputText.placeholder = "Keine Datei hochgeladen";
		}).catch( (error) => {
			// nputText.placeholder = "Fehler: " + error;
			console.log("An error occured");
		} );
	}


async function sendDeleteKnowledgeBase(knowledgeBaseId) {
	let user_response = confirm("Do you really want to delete this knowledge base?");
	if (user_response == false) {
		return;
	}

	let response = await fetch(`/generation-schemes/${knowledgeBaseId}`, { method: 'DELETE' } );

	if (!response.ok) {
		// Error
		console.log("Error occurred during abort call");
        return;
    }

	loadData()
}



</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">Knowledge Elicitation</h1> 
</div>


<div class="page-header">
    <h3 style="flex-grow: 1;">Knowledge Bases</h3> 
    <a href={`/generation-schemes/new`} use:link>
		<button style="flex-grow: 0;" >Create new</button>
	</a>
</div>


<table class="styled-table">
	<thead>
		<tr>
			<td>
				Name
			</td>
			<td>
				Base module
			</td>
			<td class="small-table-column">
				Options
			</td>
		</tr>
	</thead>
	<tbody>
{#each datas as el}
    <tr>
        <td>
			{el.name}
		</td>
		<td>
			{el.module_name}
		</td>
		<td style="white-space: nowrap; width: 1px;">
			<a href={`/generation-schemes/${el.id}/edit`} use:link>
				<button class="table-button">
					<img src="pics/edit_FILL1_wght400_GRAD0_opsz48.svg" class="table-button-icon" alt="edit"/>
				</button>
			</a>
			<button on:click={sendDeleteKnowledgeBase(el.id)} class="table-button">
				<img src="pics/delete_black_48dp.svg" class="table-button-icon" alt="delete"/>
			</button>
		</td>
	</tr>
{/each}
	</tbody>
</table>






<style>

</style>

