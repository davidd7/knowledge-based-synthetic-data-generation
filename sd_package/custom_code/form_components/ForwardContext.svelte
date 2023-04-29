<script>
	import { setContext } from 'svelte';
	export let context = {};
	setContext('context', context);
</script>

<slot/>





