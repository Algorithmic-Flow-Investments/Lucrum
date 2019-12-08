<template>
	<div class="columns">
		<div class="column">
			<Accounts></Accounts>
		</div>
		<div class="column"></div>
	</div>
</template>

<script>
import Accounts from "@/components/widgets/Accounts";
export default {
	name: "Dashboard",
	components: { Accounts, }
};
</script>

<style scoped>
</style>
