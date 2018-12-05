<template>
	<mdc-layout-grid>
		<mdc-layout-cell desktop="5" tablet="8">
			<circle-chart :values="chart" title="Total" :subtitle="total"/>
		</mdc-layout-cell>
		<mdc-layout-cell desktop="5" tablet="8" style="background: #373740">
			<accounts/>
		</mdc-layout-cell>
	</mdc-layout-grid>
</template>

<script>
  import CircleChart from "@/components/CircleChart";
  import Accounts from "@/components/Accounts";
  import { EventBus } from '../event-bus.js';

  export default {
	name: 'AccountsPage',
	components: {
	  CircleChart,
	  Accounts
	},
	data () {
	  return {
	    total: 0,
		chart: []
	  }
	},
	created() {
	  EventBus.$on('loaded/accounts', data => {
		this.total = data.subtitle;
		//this.subtitle = data.subtitle;
		this.chart = []
		let cur_total = 0
		for (let i in data.chart){
		  this.chart.push([data.chart[i][1], cur_total, cur_total + data.chart[i][0] * 3.6 - 1.5])
		  cur_total += data.chart[i][0] * 3.6
		}
	  });
	}
  }
</script>

<style scoped>

</style>
