

import Home from "./components/Home.svelte";
import Article from "./components/Article.svelte";
import NotFound from "./components/NotFound.svelte";
import GenerationSchemes from "./pages/GenerationSchemes.svelte";
import Jobs from "./pages/Jobs.svelte";

export const routes = {
  "/": Home,
  "/generation-schemes": GenerationSchemes,
  "/generation-schemes/new": Article,
  "/generation-schemes/edit": Article,
  "/jobs": Jobs,
  "/jobs/new": Article,
  "*": NotFound
};



