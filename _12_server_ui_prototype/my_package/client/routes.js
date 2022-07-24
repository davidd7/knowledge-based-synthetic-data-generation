

import Home from "./pages/Home.svelte";
// import Article from "./components/Article.svelte";
import NotFound from "./pages/NotFound.svelte";
import GenerationSchemesOverview from "./pages/GenerationSchemesOverview.svelte";
import GenerationSchemeNew from "./pages/GenerationSchemeNew.svelte";
import GenerationSchemeEdit from "./pages/GenerationSchemeEdit.svelte";
import Jobs from "./pages/JobsOverview.svelte";
import JobsNew from "./pages/JobsNew.svelte";
import ImportForms from "./forms/ImportForms.svelte"

export const routes = {
  "/": Home,
  "/generation-schemes": GenerationSchemesOverview,
  "/generation-schemes/new": GenerationSchemeNew,
  "/generation-schemes/:id/edit": GenerationSchemeEdit,
  "/jobs": Jobs,
  "/jobs/new": JobsNew,
  "*": NotFound,
  "/hidden": ImportForms
};



