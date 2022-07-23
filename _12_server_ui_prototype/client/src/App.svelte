<script>
    import Router, { link } from "svelte-spa-router";
    import { routes } from "../routes.js";
  </script>
  
  <main>
    <div style="display: flex; flex-direction: row; background: lightgrey; padding: 20px;">
        <div style="flex-grow: 0; ">
            SDGeneration
        </div>
        <div style="flex-grow: 1; text-align: center;">
            <a href={`/generation-schemes`} use:link>Generierungsschemata</a> - <a href={`/jobs`} use:link>Aufträge</a>
        </div>
        <div style="flex-grow: 0;">

        </div>
    </div>



    <Router {routes}/>
  </main>
  
  <style>
    /* @import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap"); */
  
    :global(body) {
      margin: 0;
      padding: 0px;
    }
  
    :global(a) {
      text-decoration: none;
      color: #551a8b;
    }
  
    main {
      /* max-width: 800px; */
      margin: 0 auto;
      /* font-family: "Montserrat", sans-serif; */
    }
  </style>




