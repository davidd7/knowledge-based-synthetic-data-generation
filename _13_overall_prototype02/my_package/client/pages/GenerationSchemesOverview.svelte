<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
    import Router, { link } from "svelte-spa-router";

    let datas = [];

    onMount(async () => {

        fetch('/generation-schemes', {
            method: 'GET'
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			if (response_data == "") {
				throw new Error('Something went wrong');
			}
            console.log(response_data);
			datas = response_data;
			// inputText.placeholder = "Keine Datei hochgeladen";
		}).catch( (error) => {
			// nputText.placeholder = "Fehler: " + error;
		} );
	});
</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">Generierungsschemata</h1> 
    <a href={`/generation-schemes/new`} use:link>
		<button style="flex-grow: 0;" >Neues Schema</button>
	</a>
</div>


<table class="styled-table">
	<thead>
		<tr>
			<td>
				Name
			</td>
			<td>
				Basis-Modul
			</td>
			<td class="small-table-column">
				Optionen
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
		<td class="small-table-column">
			<a href={`/generation-schemes/${el.id}/edit`} use:link>
				<button>Bearbeiten</button>
			</a>
		</td>
	</tr>
{/each}
	</tbody>
</table>








