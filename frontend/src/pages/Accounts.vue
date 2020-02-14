<template>
	<div class="columns">
		<div class="column is-5">
			<total :accounts="l_accounts" :date="hoveredDate"></total>
			<chart :accounts="l_accounts" @hover="hoveredDate=$event"></chart>
		</div>
		<div class="column is-7">
			<list></list>
		</div>
	</div>
</template>

<script>
	import Total from "@/components/Accounts/Total";
	import Chart from "@/components/Accounts/Chart";
	import * as requests from "@/helpers/requests";
	import List from "@/components/Accounts/List";

	export default {
		name: "Accounts",
		components: { List, Chart, Total },
		data() {
			return {
				hoveredDate: null
			}
		},
		methods: {
			fetch() {
				requests.get('accounts/stats/balance_graph').then(data => {
					this.l_accounts.forEach(account => {
						account.balance_graph = data[account.id]
					})
				})
			}
		},
		created() {
			this.$store.dispatch('fetch_accounts').then(() => this.l_accounts.forEach(account => account.fetch()))
			this.fetch()
		}
	};
</script>

<style scoped>

</style>
