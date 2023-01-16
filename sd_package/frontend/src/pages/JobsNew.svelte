<script>
	import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";

    let params_default = "";
    let paramsTextarea;

    let selected;
    $: {
        selected = selected;
		getDefault();
        if (paramsTextarea != null) {
            if (paramsTextarea != null && selected == undefined) {
                paramsTextarea.disabled = true;
            } else {
                paramsTextarea.disabled = false;
            }
        }
	}
    let params = params_default;
	

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
    
    async function getDefault() {
        if (selected == undefined || selected == "") {
            return;
        }
        fetch('/modules/' + document.getElementById("option_" + selected).dataset.moduleName, {
            method: 'GET'
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.json();
		}).then(response_data => {
			// sdgeneneration_schemes = response_data;
            let old_default = params_default;
            params_default = response_data.default_value;
            if (old_default == params) {
                params = params_default;
            }
		}).catch( (error) => {
			console.log( "An error occurred: " + error );
		} );
    }
		
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



	let inputFile;
    let uploadedList;

	function fileChanged() {
        if (inputFile.value == "") {
            return;
        }

		// Prepare what to send
		var formData = new FormData()
		formData.append('file', inputFile.files[0]);

        let newEl = document.createElement("LI");
        uploadedList.appendChild(newEl);
        newEl.innerHTML = "Loading..."

		fetch('/files', {
			method: 'POST',
			body: formData
		}).then(response => {
			if (!response.ok) {
				throw new Error('Something went wrong');
			}
			return response.text();
		}).then(response_data => {
			if (response_data == "") {
				throw new Error('Something went wrong');
			}
			newEl.innerHTML = `File: '${inputFile.value.replace(/.*[\/\\]/, '')}'<br>Result: Success<br>Assigned key: '${response_data}'`;
            inputFile.value = "";
		}).catch( (error) => {
            console.log("Error during file upload. If you are running flask on the dev server, use a production server instead for successfull file uploads.");
			newEl.innerHTML = `File: '${inputFile.value.replace(/.*[\/\\]/, '')}'<br>Result: Error. Please try again.`;
            inputFile.value = "";
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
            <option id={"option_" + sdgeneneration_scheme.id} value={sdgeneneration_scheme.id} data-module-name="{sdgeneneration_scheme.module_name}">
                {sdgeneneration_scheme.name}
            </option>
        {/each}
    </select>

    <p>

    <label for="paramsTextarea">Parameters:</label>
    <textarea bind:value={params} name="params" class="params-text-area" bind:this={paramsTextarea}></textarea>


    <label for="uploadedListUl">Optional: Upload files to get IDs for them and use them in the parameters:</label>
        <ul bind:this={uploadedList} name="uploadedListUl">

        </ul>
        



        
        <input bind:this={inputFile}  type="file" on:change={fileChanged}  class={"input-file"} />
        <button>
            Upload
        </button>
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





















