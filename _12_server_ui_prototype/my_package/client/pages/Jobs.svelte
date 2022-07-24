<script>
    import urlSlug from "url-slug";
    
</script>


<div class="page-header">
    <h1 style="flex-grow: 1;">Aufträge</h1> 
    <button style="flex-grow: 0;">Neuer Auftrag</button>
</div>




<table class="styled-table">
	<thead>
		<tr>
			<td>
				ID
			</td>
			<td>
				Schema
			</td>
			<td>
				Datum
			</td>
			<td class="small-table-column">
				Optionen
			</td>
		</tr>
	</thead>
	<tbody>
{#each [] as el}
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





















