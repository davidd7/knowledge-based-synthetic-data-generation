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
    import {location, querystring} from 'svelte-spa-router'


let x = {aaa : 50};

export const routes = {
  "/": wrap({component: Home, conditions: [ (detail)=>{
    // console.log(detail.location);
    // console.log( $location );
    // console.log( $querystring );
    console.log(GenerationSchemeEdit.checkState);
    console.log(GenerationSchemeEdit.params);
    console.log(GenerationSchemeEdit);
    console.log(x);
    console.log(x.aaa());
  } ],
  props: {
            num: x
        }
      }
  ),
  "/generation-schemes": GenerationSchemesOverview,
  "/generation-schemes/new": GenerationSchemeNew,
  "/generation-schemes/:id/edit": wrap({component: GenerationSchemeEdit, props: { num: x } } ),
  "/jobs": Jobs,
  "/jobs/new": JobsNew,
  "*": NotFound
};




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
  <Router {routes}/>
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




