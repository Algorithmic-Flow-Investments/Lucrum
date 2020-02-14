<template>
	<segment colour="red"
			 :amount="account.calculated_balance"
			 :title="account.name"
			 :subtitle="account.description"
			 ref="segment">
	</segment>
</template>

<script>
	import Account from "@/Models/Account";
	import Segment from "@/components/Segment";

	export default {
		name: "AccountSegment",
		components: { Segment },
		props: {
			account: Account
		}
	};
</script>

<style scoped>

</style>
