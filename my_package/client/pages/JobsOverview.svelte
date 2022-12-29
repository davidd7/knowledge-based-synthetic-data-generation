<script>
	import { onMount } from 'svelte';
    import Router, { link, push } from "svelte-spa-router";
    // import { push } from "svelte-spa-router";

    let jobs = [];

    onMount(async () => {
		loadData();
    });


function loadData() {
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
}


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



async function sendAbort(jobId) {
	let response = await fetch(`/jobs/${jobId}/abort`, { method: 'POST' } );

	if (!response.ok) {
		// Error
		console.log("Error occurred during abort call");
        return;
    }
        
	response_data = await response.json();
	console.log(response_data);
}



async function sendDelete(jobId) {
	let response = await fetch(`/jobs/${jobId}`, { method: 'DELETE' } );

	if (!response.ok) {
		// Error
		console.log("Error occurred during abort call");
        return;
    }

	loadData()
}



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
			<!-- {#if job.status == "generating"}
				<button on:click={sendAbort(job.id)}>Abort</button>
			{/if} -->
			{#if job.status == "finished"}
				<a href={`/jobs/${job.id}/result`} download>
					<button >Download</button>
				</a>
			{/if}
			{#if job.status == "finished" || job.status == "aborted" || job.status == "unknown" }
			<button on:click={sendDelete(job.id)}>Delete</button>
			{/if}
			{#if job.status == "finished" }
			<button on:click={alert(job.statistics)}>Statistics</button>
			{/if}
		</td>
	</tr>
{/each}
	</tbody>
</table>





















