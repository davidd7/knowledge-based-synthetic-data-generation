<script>
	import { onMount } from 'svelte';
    import Router, { link } from "svelte-spa-router";

    let jobs = [];

    onMount(async () => {
        fetch('/jobs', {
            method: 'GET'
        }).then(response => {
            if (!response.ok) {
                throw new Error('Something went wrong');
            }
            return response.json();
        }).then(response_data => {
            console.log(response_data);
            jobs = response_data;
        }).catch( (error) => {
            console.log( "An error occured: " + error );
        } );
    });


function date_custom_format(date) {
    function two_digit(number) {
        return (number > 9 ? "" : "0") + number
    }

    var mm = two_digit(date.getMonth() + 1); // getMonth() is zero-based
    var dd = two_digit(date.getDate());
    let hh = two_digit(date.getHours());
    let min = two_digit(date.getMinutes());
    let ss = two_digit(date.getSeconds());

    return `${date.getFullYear()}-${mm}-${dd} ${hh}:${min}:${ss}`;
};






</script>


<div class="page-header">
    <h1 style="flex-grow: 1;">Aufträge</h1> 
    <a href={`/jobs/new`} use:link>
        <button style="flex-grow: 0;">Neuer Auftrag</button>
    </a>
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
				Status
			</td>
		</tr>
	</thead>
	<tbody>
{#each jobs as job}
    <tr>
        <td>
			{job.id}
		</td>
		<td>
			{job.scheme_name}
		</td>
		<td>
			{date_custom_format(new Date(job.creation_date))}
		</td>
		<td class="small-table-column">
            {job.status}
			<!-- <a href={`/jobs`} use:link>
				<button>Bearbeiten</button>
			</a> -->
		</td>
	</tr>
{/each}
	</tbody>
</table>





















