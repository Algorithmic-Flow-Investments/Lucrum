<template>
	<div ref="sect" class="sect">
		<AccountSegment v-for="(account, i) in l_accounts" :account="account"></AccountSegment>
	</div>
</template>

<script>
	import AccountSegment from "@/components/Accounts/AccountSegment";
	export default {
		name: "List",
		components: { AccountSegment },
	};
</script>

<style scoped>
	.sect {
		height: calc(100vh - 24px);
		overflow-y: scroll;
		padding-top: 10px;
	}
</style>
