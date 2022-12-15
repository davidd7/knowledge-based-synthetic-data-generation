
<script>
	export let headline = "";
</script>


<div class="headlinedGroup">
	<h3>
		{headline}
	</h3>
	<div class="indented-block">
		<slot/>
	</div>
</div>


<style>
	.headlinedGroup {
	}
	.indented-block {
		margin-left: 36px;
	}
</style>



