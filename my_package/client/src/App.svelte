<script>
    import Router, { link } from "svelte-spa-router";
    import { routes } from "../routes.js";
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




