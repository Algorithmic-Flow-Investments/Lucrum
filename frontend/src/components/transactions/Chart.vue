<template>
	<div>
		<div class="chart" ref="wrapper">
			<transition name="fade" mode="out-in">
				<donut v-if="circle" :data="pie">
					<div>Spent</div>
					<br/>
					<br/>
					<div class="main money">{{ '£' + Math.round(-tweenTotal) }}</div>
					<br/>
					<br/>
					<br/>
				</donut>
				<alt-chart v-else-if="graph.length > 0" :graph="graph" :top="top" :height="graphHeight"></alt-chart>
			</transition>
		</div>
		<toggle-chart v-model="circle" one="chart-pie" two="chart-line" @budget="setBudget"></toggle-chart>
	</div>
</template>

<script>
import Donut from "@/components/charts/Donut";
import * as requests from "@/helpers/requests"
import AltChart from "@/components/transactions/AltChart";
import moment from "moment";
import ToggleChart from "@/components/charts/ToggleChart";

export default {
	name: "chart",
	props: ["stats", "range", "top"],
	components: { ToggleChart, AltChart, Donut },
	data() {
		return {
			circle: true,
			graph: [],
			tweenTotal: this.stats.gross.total || 0,
			budget: JSON.parse(localStorage.selected_budget || null)
		};
	},
	methods: {
		fetch() {
			if (this.range.min === null || this.range.max === null) return;
			requests.get('transactions/graph', {
				params: {
					min: this.range.min.format("YYYY-M-D"),
					max: this.range.max.format("YYYY-M-D"),
					budget: this.budget.id
				}
			}).then(data => {
				this.graph = data
				if (this.range.frame === "month") {
					while (this.graph.length < 31) {
						this.graph.push({ amount: 0, date: this.graph.length + 1 })
					}
				}
			})
		},
		setBudget(budget){
			this.budget = budget
			this.fetch()
			this.$emit('budget', budget)
		}
	},
	watch: {
		'stats.gross.total': function() {
			let jump = (this.stats.gross.total - this.tweenTotal) / 100
			let tween = setInterval(() => {
				if (Math.abs(this.tweenTotal - this.stats.gross.total) < 16) {
					this.tweenTotal = this.stats.gross.total
					clearInterval(tween)
					return
				}
				this.tweenTotal += jump
			}, 10)
		}
	},
	computed: {
		graphHeight() {
			if (!this.$refs.wrapper) return 300;
			return this.$refs.wrapper.clientHeight
		},
		pie () {
			//let chart = Object.keys(this.stats.categories).map(key => {
			//	return {title: key, value: this.stats.categories[key].total, colour: '#ff0000'}
			//})
			if (this.stats.categories === {}) return [];
			let chart = [];
			Object.keys(this.stats.categories).forEach(key => {
				let total = this.stats.categories[key].total;
				if (total < 0) {
					let tags = []
					Object.keys(this.stats.categories[key].tags).forEach(tag_key => {
						let tag_total = this.stats.categories[key].tags[tag_key].total
						if (tag_total < 0){
							tags.push({title: tag_key, value: -tag_total, colour: '#00ff00'})
						}
					})
					chart.push({title: key, value: -total, colour: '#ff0000', children: tags})
				}
			});
			chart.sort((a, b) => b.value - a.value);
			return chart
		}
	},
	created() {
		this.fetch()
	}
};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";

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
