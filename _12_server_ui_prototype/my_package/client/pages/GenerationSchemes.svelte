<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
    import Router, { link } from "svelte-spa-router";
    import { routes } from "../routes.js";
    // import { format } from "timeago.js";
    // import Card from "./Card.svelte";
    // import { blogs } from "../data.js";

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




		// const res = await fetch(`/tutorial/api/album`);
		// photos = await res.json();
	});
    
		


</script>
    


<div class="page-header">
    <h1 style="flex-grow: 1;">Generierungsschemata</h1> 
    <a href={`/generation-schemes/new`} use:link><button style="flex-grow: 0;" >Neues Schema</button></a>
</div>


{#each datas as el}
    <div>
        {el.name}, {el.module_name} <button>Edit</button>
    </div>
{/each}