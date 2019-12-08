<template>
	<div class="columns">
		<div class="column is-5">
			<date-select v-model="range" :target="targetDate" @input="update()"/>
			<chart ref="chart" :stats="stats" :range="range" :top="topTransaction" @budget="setBudget"/>
			<stats :stats="stats" />
		</div>
		<div class="column is-7">
			<list ref="list" :range="range" :categories="budget.categories" @scroll="topTransaction=$event" />
		</div>
	</div>
</template>

<script>
import Chart from "@/components/transactions/Chart";
import Stats from "@/components/transactions/Stats";
import List from "@/components/transactions/List";
import DateSelect from "@/components/transactions/DateSelect";

import * as requests from "@/helpers/requests"
import moment from "moment";

export default {
	name: "Transactions",
	components: { DateSelect, List, Stats, Chart },
	data() {
		return {
			range: { min: null, max: null },
			targetDate: null,
			topTransaction: null,
			stats: {
				gross: {},
				income: {},
				outgoing: {},
				categories: {}
			},
			budget: JSON.parse(localStorage.selected_budget || null)
		};
	},
	methods: {
		update() {
			this.$nextTick(() => {
				this.$refs.list.fetch();
				this.$refs.chart.fetch();
				this.fetch()
			})
		},
		fetch() {
			if (this.range.min === null || this.range.max === null) return;
			requests.get('transactions/stats', {
				params: {
					min: this.range.min.format("YYYY-M-D"),
					max: this.range.max.format("YYYY-M-D"),
					budget: this.budget.id
				}
			}).then(data => {
				this.stats = data
			})
		},
		setBudget(budget){
			this.budget = budget
			this.fetch()
		}
	},
	created() {
		this.fetch()
		this.targetDate = moment(this.$route.query.date)
	}
};
</script>

<style scoped></style>
