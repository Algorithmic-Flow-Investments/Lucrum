<template>
	<div class="columns">
		<div class="column is-5">
			<total :accounts="accounts" :date="hoveredDate"></total>
			<Chart :accounts="accounts" @hover="hoveredDate=$event"></Chart>
		</div>
		<div class="column is-7">
		</div>
	</div>
</template>

<script>
	import Total from "@/components/Accounts/Total";
	import * as requests from "@/helpers/requests"
	import Chart from "@/components/Accounts/Chart";

	export default {
		name: "Accounts",
		components: { Chart, Total },
		data() {
			return {
				accounts: [],
				hoveredDate: null
			}
		},
		methods: {
			fetch(){
				requests.get('accounts/list/advanced').then(accounts => {
					this.accounts = accounts
				})
			}
		},
		created() {
			this.fetch()
		}
	};
</script>

<style scoped>

</style>
