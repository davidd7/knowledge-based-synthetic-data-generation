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


  let hasUnsavedDataDefault = () => false;
  let x = {hasUnsavedData : hasUnsavedDataDefault};

function allPagesCondition(detail) {
  if ( x.hasUnsavedData() ) {
    // alert();
    // push('/book/42');
    // pop();
    // replace('/generation-schemes/15/edit');
    // detail.location = '/generation-schemes/15/edit';
    return false;
  } else {
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
        replace('/generation-schemes/15/edit')
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




