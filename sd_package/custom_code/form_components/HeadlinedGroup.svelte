<script>
	export let headline = "";
</script>


<div>
	<h3>
		{headline}
	</h3>
	<div class="indented-block">
		<slot/>
	</div>
</div>


<style>
	.indented-block {
		margin-left: 36px;
	}
</style>



