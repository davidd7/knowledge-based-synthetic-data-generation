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
            console.log( "An error occurred: " + error );
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
    <h1 style="flex-grow: 1;">Data Generation</h1> 
</div>

<span>
All data generation commands can also be executed automatically via the API.
</span>

<div class="page-header">
    <h3 style="flex-grow: 1;">Generation Jobs</h3> 
    <a href={`/jobs/new`} use:link>
        <button style="flex-grow: 0;">Start new</button>
    </a>
</div>



<table class="styled-table">
	<thead>
		<tr>
			<td>
				ID
			</td>
			<td>
				Base knowledge base
			</td>
			<td>
				Base module
			</td>
			<td>
				Date
			</td>
			<td class="small-table-column">
				State
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
			{job.module_name}
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





















