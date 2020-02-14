<template>
	<div>
		<div class="chart" ref="wrapper">
			<transition name="fade" mode="out-in">
				<tags-categories-chart v-if="circle" :stats="stats" :chart="tagsChart" @tagcat="setTagCat"></tags-categories-chart>
				<outgoings-chart v-else-if="graph.length > 0" :graph="outgoingsChart" :top="top" :height="graphHeight"></outgoings-chart>
			</transition>
		</div>
		<toggle-chart v-model="circle" one="chart-pie" two="chart-line" @budget="setBudget"></toggle-chart>
	</div>
</template>

<script>
import Donut from "@/components/charts/Donut";
import * as requests from "@/helpers/requests"
import OutgoingsChart from "@/components/transactions/charts/OutgoingsChart";
import moment from "moment/moment";
import ToggleChart from "@/components/charts/ToggleChart";
import TagsCategoriesChart from "@/components/transactions/charts/TagsCategoriesChart";

export default {
	name: "ChartWrapper",
	props: ["stats", "range", "top"],
	components: { TagsCategoriesChart, ToggleChart, OutgoingsChart },
	data() {
		return {
			circle: true,
			budget: JSON.parse(localStorage.selected_budget || null),
			tagsChart: {},
			outgoingsChart: [],
		};
	},
	methods: {
		fetch() {
			if (this.range.min === null || this.range.max === null) return;
			// requests.get('transactions/graph', {
			// 	params: {
			// 		min: this.range.min.format("YYYY-M-D"),
			// 		max: this.range.max.format("YYYY-M-D"),
			// 		budget: this.budget.id
			// 	}
			// }).then(data => {
			// 	this.graph = data
			// 	if (this.range.frame === "month") {
			// 		while (this.graph.length < 31) {
			// 			this.graph.push({ amount: 0, date: this.graph.length + 1 })
			// 		}
			// 	}
			// })
			requests.get('transactions/stats/tags_categories', {
				params: {
					min: this.range.min.format("YYYY-M-D"),
					max: this.range.max.format("YYYY-M-D"),
					budget: this.budget.id
				}
			}).then(data => {
				this.tagsChart = data
			})
		},
		setBudget(budget_id){
			this.fetch()
			this.$emit('budget', budget_id)
		},
		setTagCat(selected) {
			this.$emit('tagcat', selected)
		}
	},
	computed: {
		graphHeight() {
			if (!this.$refs.wrapper) return 300;
			return this.$refs.wrapper.clientHeight
		},
	},
	created() {
		this.fetch()
	}
};
</script>

<style scoped lang="scss">
	@import "../../../assets/colours";

	.main {
		font-size: 52px;
		color: $text-strong;
	}

	.chart {
		height: 40vh;
	}

	.fade-enter-active, .fade-leave-active {
		transition: opacity .25s;
	}
	.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
		opacity: 0;
	}
</style>
