<script>
	import { onMount, onDestroy  } from 'svelte';
    import Router, { link, push } from "svelte-spa-router";
    // import { push } from "svelte-spa-router";

    let jobs = [];

    onMount(async () => {
		loadData();
    });


    onDestroy(async () => {
		console.log("ondestroy");
		source.close();
    });


let source = new EventSource('/jobs/updates-stream');
let lastUpdateCount = undefined;

function loadData() {
	fetch('/jobs', {
            method: 'GET'
        }).then(response => {
            if (!response.ok) {
                throw new Error('Something went wrong');
            }
            return response.json();
        }).then(response_data => {
            // console.log(response_data);
            jobs = response_data;
        }).catch( (error) => {
            console.log( "An error occurred: " + error );
        } );

	source.onmessage = function (event) {
		//  alert(event.data);
		console.log(event.data);
		if (lastUpdateCount == undefined || lastUpdateCount != event.data) {
			lastUpdateCount = event.data;
			loadData();
		}
	};
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
	let user_response = confirm("Do you really want to delete this knowledge base?");
	if (user_response == false) {
		return;
	}

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
				Status
			</td>
			<td class="small-table-column">
				Options
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
		</td>
		<td style="white-space: nowrap; width: 1px; text-align: right;">
			<!-- {#if job.status == "generating"}
				<button on:click={sendAbort(job.id)}>Abort</button>
			{/if} -->
			{#if job.status == "finished"}
				<a href={`/jobs/${job.id}/result`} download>
					<button class="table-button">
						<img src="pics/file_download_black_48dp.svg" class="table-button-icon" alt="download"/>
					</button>
				</a>
			{/if}
			{#if job.status == "finished" }
				<button on:click={alert(job.statistics)} class="table-button">
					<img src="pics/query_stats_black_48dp.svg" class="table-button-icon" alt="view statistics"/>
				</button>
			{/if}
			{#if job.status == "finished" || job.status == "aborted" || job.status == "unknown" || job.status == "error" }
				<button on:click={sendDelete(job.id)} class="table-button">
					<img src="pics/delete_black_48dp.svg" class="table-button-icon" alt="delete"/>
				</button>
			{/if}
		</td>
	</tr>
{/each}
	</tbody>
</table>





















