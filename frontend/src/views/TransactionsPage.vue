<template>
	<div>
		<mdc-layout-inner-grid>
			<mdc-layout-cell desktop="6">
				<date-select v-model="range" :target="targetDate"></date-select>
				<transactions-chart :stats="stats" :graph="graph"></transactions-chart>
				<stats-segment :stats="stats"></stats-segment>
			</mdc-layout-cell>
			<mdc-layout-cell class="transactionsList" desktop="6" tablet="8">
				<transactions :min="range.min" :max="range.max"/>
			</mdc-layout-cell>
		</mdc-layout-inner-grid>
	</div>
</template>

<script>
import Transactions from "@/components/transactions/Transactions";
import DateSelect from "@/components/DateSelect";
import TransactionsChart from "@/components/transactions/TransactionsChart"
import StatsSegment from "@/components/transactions/StatsSegment"

import axios from "axios";
import moment from "moment";

export default {
	name: "TransactionsPage",
	components: {
		Transactions,
		TransactionsChart,
		DateSelect,
		StatsSegment
	},
	data() {
		return {
			range: { min: null, max: null },
			stats: {
				gross: {},
				income: {},
				outgoing: {}
			},
			targetDate: null,
			graph: []
		};
	},
	watch: {
		range: function() {
			this.fetchData();
		}
	},
	methods: {
		fetchData() {
			if (this.range.min == null || this.range.max == null) return;
			axios
				.get(window.APIROOT + "api/transactions/stats", {
					params: {
						min: this.range.min.format("YYYY-M-D"),
						max: this.range.max.format("YYYY-M-D")
					}
				})
				.then(response => {
					this.stats = response.data;
				});

			axios
				.get(window.APIROOT + "api/transactions/graph", {
					params: {
						min: this.range.min.format("YYYY-M-D"),
						max: this.range.max.format("YYYY-M-D")
					}
				})
				.then(response => {
					this.graph = response.data;
				});
		},
		getRange(){
			if (this.$route.params.transactionId) {
				axios.get(window.APIROOT + 'api/transaction/' + this.$route.params.transactionId).then(response => {
					let date = moment(response.data.date)
					this.targetDate = date
				})
			}
		}
	},
	created() {
		this.getRange()
	},
	mounted() {
		this.fetchData();
	}
};
</script>

<style scoped>
.transactionsList {
	background: #373740;
	overflow-y: scroll;
	/*overflow-x: hidden;*/
	height: calc(100vh - 96px);
}
</style>
