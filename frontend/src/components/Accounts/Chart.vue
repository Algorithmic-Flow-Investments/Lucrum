<template>
	<!--la-cartesian :data="graph">
		<defs>
			<linearGradient id="color-id" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stop-color="#2c3e50"></stop>
				<stop offset="0.5" stop-color="#42b983"></stop>
				<stop offset="1" stop-color="#6fa8dc"></stop>
			</linearGradient>
		</defs>
		<la-line curve :width="2" prop="value" color="url(#color-id)"></la-line>
		<la-x-axis :interval="4"></la-x-axis>
		<la-y-axis :nbTicks="8"></la-y-axis>
	</la-cartesian-->
	<apexchart v-if="series" type="area" height="350" :options="chartOptions" :series="series" @mouseleave.native="$emit('hover', null)" />
</template>

<script>
import moment from "moment";
import VueApexCharts from "vue-apexcharts";

export default {
	name: "Chart",
	props: ["accounts"],
	components: {
		apexchart: VueApexCharts
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
	},
	computed: {
		series() {
			if (this.accounts.length === 0) return;
			let series = [];
			this.accounts.forEach(account => {
				let date = moment();
				let graph = []
				for (let i = 0; i < 52 * 2; i++) {
					let total = this.account_balance(account, date);
					graph.unshift([date.format('YYYY/MM/DD'), total]);
					date.subtract(7, "days");
				}
				series.unshift({data: graph, name: account.name})
			})
			return series;
		}
	},
	data() {
		return {
			chartOptions: {
				dataLabels: {
					enabled: false
				},
				chart: {
					stacked: true,
					toolbar: {
						show: false
					},
				},
				markers: {
					size: 0,
					style: "hollow"
				},
				xaxis: {
					type: "datetime",
					tickAmount: 6,
					labels: {
						style: {
							colors: 'white'
						}
					},
					tooltip: {
						enabled: false
					}
				},
				legend: {
					show: false
				},
				yaxis: {
					labels: {
						style: {
							color: 'white'
						},
						formatter: (val, index) => {
							return Math.round(val / 1000) + "K"
						}
					},
				},
				grid: {
					yaxis: {
						lines: {
							show: false
						}
					},

				},
				tooltip: {
					x: {
						formatter: (time, { series, seriesIndex, dataPointIndex, w }) => {
							if (!seriesIndex) return ""
							let total = series.reduce((total, account) => {
								return total + account[dataPointIndex]
							}, 0)
							let mTime = moment(time)
							this.$emit('hover', mTime)
							return mTime.format("Do MMM YYYY") + " - £" + Math.round(total)
						}
					},
					y: {
						formatter: (val) => {
							if (val === 0) return null
							return val
						}
					},
				},
				fill: {
					type: "gradient",
					gradient: {
						shadeIntensity: 1,
						opacityFrom: 0.7,
						opacityTo: 0.9,
						stops: [0, 100]
					}
				},
				stroke: {
					width: 1
				}
			},
		};
	}
};
</script>

<style scoped></style>
