<script>
    import urlSlug from "url-slug";
	import { onMount } from 'svelte';
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
    
YAY


 <h1>Generierungsschemata</h1>
{#each datas as el}
    <div>
        {el.name}, {el.module_name} <button>Edit</button>
    </div>
{/each}