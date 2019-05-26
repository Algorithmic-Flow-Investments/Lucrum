<template>
	<div>
		<circle-chart v-if="circle" :values="[['#ff0000', 0, 359]]">
			<mdc-text typo="subtitle1" tag="span" adjust-margin>Total</mdc-text>
			<br />
			<mdc-text typo="headline3" tag="span" adjust-margin>{{ '£' + Math.round(stats.gross.total) }}</mdc-text>
			<br />
			<br />
			<mdc-text typo="subtitle1" tag="span" adjust-margin>Spending</mdc-text>
			<br />
			<mdc-text typo="headline3" tag="span" adjust-margin>{{ '£' + Math.round(stats.outgoing.total) }}</mdc-text>
			<br />
			<!--mdc-icon icon="info_outline"></mdc-icon-->
		</circle-chart>
		<div v-else-if="max_amount > 0">
			<la-cartesian autoresize :bound="[0]" :data="graph">
				<defs>
					<linearGradient id="area-fill" x1="0" y1="0" x2="0" y2="1">
						<stop stop-color="#0076b1" offset="0%" stop-opacity="0.4"></stop>
						<stop stop-color="#0076b1" offset="50%" stop-opacity="0.2"></stop>
						<stop stop-color="#0076b1" offset="100%" stop-opacity="0"></stop>
					</linearGradient>
				</defs>
				<la-area fill-color="url(#area-fill)" dot curve prop="amount"></la-area>
				<la-x-axis prop="date"></la-x-axis>
				<la-y-axis :ticks="graph_ticks"></la-y-axis>
				<la-y-marker dashed :value="average_per_subdivision" label="Avg. per day"></la-y-marker>
				<la-tooltip></la-tooltip>
			</la-cartesian>
		</div>
		<button @click="circle=!circle">toggle</button>
	</div>
</template>

<script>
	import CircleChart from "@/components/CircleChart";
	import { Cartesian, Area, XAxis, YAxis, Tooltip, YMarker } from "laue"
	import moment from 'moment'



	export default {
		name: "TransactionsChart",
		props: ['stats', 'graph'],
		data() {
			return {
				circle: false,
			}
		},
		components: {
			CircleChart,
			LaCartesian: Cartesian,
			LaArea: Area,
			LaXAxis: XAxis,
			LaYAxis: YAxis,
			LaTooltip: Tooltip,
			LaYMarker: YMarker
		},
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
				}, 0) / this.graph.length
			}
		}
	}
</script>

<style scoped>

</style>
