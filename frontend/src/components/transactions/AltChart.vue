<template>
	<la-cartesian autoresize :bound="[0]" :data="graph" :height="height">
		<defs>
			<linearGradient id="area-fill" x1="0" y1="0" x2="0" y2="1">
				<stop stop-color="#0076b1" offset="0%" stop-opacity="0.4"></stop>
				<stop stop-color="#0076b1" offset="50%" stop-opacity="0.2"></stop>
				<stop stop-color="#0076b1" offset="100%" stop-opacity="0"></stop>
			</linearGradient>
		</defs>
		<la-area animated continued :animationDuration="2" fill-color="url(#area-fill)" dot prop="amount"></la-area>
		<la-x-axis prop="date"></la-x-axis>
		<la-y-axis :ticks="graph_ticks"></la-y-axis>
		<la-y-marker animated dashed :value="average_per_subdivision" :label="'Avg. per day: £' + numberWithCommas(average_per_subdivision)"></la-y-marker>
		<la-x-marker animated :value="curDate" color="rgba(255, 0, 0, 0.5)"></la-x-marker>
		<la-tooltip></la-tooltip>
	</la-cartesian>
</template>

<script>
	import moment from "moment";
	import LaXMarker from "@/components/charts/la-x-marker";
	export default {
		name: "AltChart",
		components: { LaXMarker },
		props: ["graph", "top", "height"],
		computed: {
			graph_ticks() {
				let numTicks = 5
				let ticks = []
				for (let i=0; i < numTicks + 1; i++){
					ticks.push(Math.round(this.max_amount / numTicks * i))
				}
				return ticks
			},
			max_amount() {
				return Math.max.apply(Math, this.graph.map(function(point) { return point.amount; }))
			},

			average_per_subdivision(){
				return this.graph.reduce((total, cur) => {
					return total + cur.amount
				}, 0) / this.graph.filter(item => item.amount !== null).length
			},
			curDate(){
				if (!this.top) return null;
				let date = moment(this.top.date)
				let lastDate = this.graph.filter(item => {
					return item.amount > 0
				}).pop().date
				if (date.date() >= lastDate) return null;
				return date.date()
			}
		},
		methods: {
			numberWithCommas(x) {
				return parseFloat(x)
					.toFixed(2)
					.toString()
					.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
			}
		}
	};
</script>

<style scoped>

</style>
