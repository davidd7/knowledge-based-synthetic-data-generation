<script>
  import Router, { link } from "svelte-spa-router";
  // import { routes } from "./routes.js";
  import GlobalOverflowMenu from "./GlobalOverflowMenu.svelte";
  import MenuButton from './MenuButton.svelte';

  import Home from "./pages/Home.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import GenerationSchemesOverview from "./pages/GenerationSchemesOverview.svelte";
  import GenerationSchemeNew from "./pages/GenerationSchemeNew.svelte";
  import GenerationSchemeEdit from "./pages/GenerationSchemeEdit.svelte";
  import Jobs from "./pages/JobsOverview.svelte";
  import JobsNew from "./pages/JobsNew.svelte";

  import {wrap} from 'svelte-spa-router/wrap'
  import {push, pop, replace, location, querystring} from 'svelte-spa-router'
	import { onDestroy, onMount } from 'svelte';



  
	onDestroy( () => {
		window.removeEventListener("beforeunload", browserSaveBeforeLeave);
	} );


  
	function browserSaveBeforeLeave(e) {
    if ( x.hasUnsavedData() ) {
			var confirmationMessage = 'It looks like you have been editing something. '
									+ 'If you leave before saving, your changes will be lost.';

			(e || window.event).returnValue = confirmationMessage; //Gecko + IE
			return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
    	}
    }


  onMount( () => {
		window.addEventListener("beforeunload", browserSaveBeforeLeave);
	} );


  let hasUnsavedDataDefault = () => false;
  let x = {hasUnsavedData : hasUnsavedDataDefault};

function allPagesCondition(detail) {
  if ( x.hasUnsavedData() ) {
    console.log("Leaving page although there are unsaved changes (no way to stop the page leaving with svelte-spa-router at the moment).");
    x.hasUnsavedData = hasUnsavedDataDefault; // remove the save tester, because we're not staying on page anyway (would leave it if the page could be not left)
    return true; // set to true so that new page loads (if false then would load blank page but still leave the old page)
  } else {
    console.log("Leaving page, everything okay.");
    x.hasUnsavedData = hasUnsavedDataDefault;
    return true;
  }
}

export const routes = {
  "/": wrap({component: Home, conditions: [ allPagesCondition ] } ),
  "/generation-schemes": wrap({component: GenerationSchemesOverview, conditions: [ allPagesCondition ] } ),
  "/generation-schemes/new": wrap({component: GenerationSchemeNew, conditions: [ allPagesCondition ] } ),
  "/generation-schemes/:id/edit": wrap({component: GenerationSchemeEdit, props: { num: x }, conditions: [ allPagesCondition ] } ),
  "/jobs": wrap({component: Jobs, conditions: [ allPagesCondition ] } ),
  "/jobs/new": wrap({component: JobsNew, conditions: [ allPagesCondition ] } ),
  "*": wrap({component: NotFound, conditions: [ allPagesCondition ] } )
};



function conditionsFailed(event) {
    console.error('conditionsFailed event', event.detail)

    // Perform any action, for example replacing the current route
    // if (event.detail.userData.foo == 'bar') {
    //     replace('/hello/world')
    // }
        // replace('/generation-schemes/15/edit')
}


</script>
  
<nav>
  <div class="nav-container">
      <div style="flex-grow: 0; ">
        <a href={`/`} use:link>SDGeneration</a>
      </div>
      <div style="flex-grow: 1; text-align: center;">
          <a href={`/modules`} use:link>Configuration</a> - 
          <a href={`/generation-schemes`} use:link>Knowledge Elicitation</a> - 
          <a href={`/jobs`} use:link>Data Generation</a>
      </div>
      <div style="flex-grow: 0;">
        <MenuButton>
          <GlobalOverflowMenu/>
        </MenuButton>
      </div>
    </div>
</nav>

<main>
  <Router {routes} on:conditionsFailed={conditionsFailed}/>
</main>

  
  <style>
    :global(body) {
      margin: 0;
      padding: 0px;
    }
  
    :global(a) {
      text-decoration: none;
      color: #551a8b;
    }

    a {
      color: black;
    }

    .nav-container {
      display: flex;
      flex-direction: row;
      background: lightgray;
      padding: 20px;
      box-shadow: 0 0 3px rgba(0, 0, 0, 0.15);
    }
  </style>




