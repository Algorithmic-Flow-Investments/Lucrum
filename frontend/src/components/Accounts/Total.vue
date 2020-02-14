<template>
	<div class="sect">
		<proportional-header :total="total" title="total" :chart="chart"></proportional-header>
	</div>
</template>

<script>
	import ProportionalHeader from "@/components/widgets/ProportionalHeader";
	import moment from "moment";
	export default {
		name: "Total",
		components: { ProportionalHeader },
		props: ["accounts", "date"],
		data() {
			return {
				chart: []
			}
		},
		computed: {
			total() {
				let date = this.date || moment()
				return this.graph[date.format('YYYY-MM-DD')]
			},
			graph() {
				let date = moment();
				let graph = {}
				for (let i = 0; i < 52 * 2; i++) {
					let total = this.accounts.reduce((total, account) => {
						return total + this.account_balance(account, date)
					}, 0)
					graph[date.format('YYYY-MM-DD')] = total;
					date.subtract(7, "days");
				}
				return graph
			}
		},
		methods: {
			account_balance(account, date) {
				if (!account.balance_graph) return 0;
				let dates = Object.keys(account.balance_graph);
				let closest_date = dates.filter(d => {
					return moment(d).isSameOrAfter(date);
				})[0];
				return account.balance_graph[closest_date];
			}
		}
	};
</script>

<style scoped>

</style>
