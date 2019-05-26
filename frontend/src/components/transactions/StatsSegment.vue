<template>
	<div style="color: white; font-family: 'Roboto Condensed', sans-serif">
		<h2>Gross income</h2>
		<div>Total: {{stats.gross.total | round}}</div>
		<div>{{stats.gross.prev_range_diff.percent | round}}% compared with last period</div>
		<div>{{stats.gross.prev_all_diff.percent | round}}% compared with all time average</div>
		<h2>Net Income</h2>
		<div>Total: {{stats.income.total | round}}</div>
		<div>{{stats.income.prev_range_diff.percent | round}}% compared with last period</div>
		<div>{{stats.income.prev_all_diff.percent | round}}% compared with all time average</div>
		<h2>Net Outgoing</h2>
		<div>Total: {{stats.outgoing.total | round}}</div>
		<div>{{stats.outgoing.prev_range_diff.percent | round}}% compared with last period</div>
		<div>{{stats.outgoing.prev_all_diff.percent | round}}% compared with all time average</div>
		<h2>Average per subdivision</h2>
		<div>Gross: {{stats.gross.total | average_per_subdivision(stats)}}</div>
		<div>Income: {{stats.income.total | average_per_subdivision(stats)}}</div>
		<div>Outgoing: {{stats.outgoing.total | average_per_subdivision(stats)}}</div>
	</div>
</template>

<script>
	import moment from 'moment'

	export default {
		name: "StatsSegment",
		props: ['stats'],
		filters: {
			round(value){
				return Math.round(value)
			},
			average_per_subdivision(amount, stats){
				let first_date = moment(stats.first_date)
				let last_date = moment(stats.last_date)
				let duration = moment.duration(last_date.diff(first_date));
				let divisor;
				if (duration.days() <= 7) {
					divisor = 7
				}
				else if (duration.days() <= 31) {
					divisor = duration.days() / 7
				}
				else {
					divisor = duration.days() / 30
				}

				return amount / divisor
			}
		},
		computed: {

		}
	}
</script>

<style scoped>

</style>
