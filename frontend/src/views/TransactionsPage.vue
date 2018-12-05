<template>
	<div>
		<mdc-tab-bar @change="onSelected">
			<mdc-tab>Week</mdc-tab>
			<mdc-tab active>Month</mdc-tab>
			<mdc-tab>Year</mdc-tab>
		</mdc-tab-bar>
		<div class="dateSelect">
			<mdc-icon icon="chevron_left" @click.native="subDate" style="color: #AEAEB1;line-height: 20px;vertical-align: top;"></mdc-icon>
			<span v-if="timeFrame == 'year'" class="timeFrame">{{endDateSnapped.format('YYYY')}}</span>
			<span v-if="timeFrame == 'month'" class="timeFrame">{{endDateSnapped.format('MMMM, YYYY')}}</span>
			<span v-if="timeFrame == 'week'" class="timeFrame">{{startDate.format('D MMM') + ' - ' + endDateSnapped.format('D MMM YY')}}</span>
			<mdc-icon v-if="now > endDateSnapped" @click.native="addDate" icon="chevron_right" style="color: #AEAEB1;line-height: 20px;vertical-align: top;"></mdc-icon>
		</div>

	<mdc-layout-grid>
		<mdc-layout-cell>
			CHART
		</mdc-layout-cell>
		<mdc-layout-cell class="transactionsList" desktop="5" tablet="8">
			<transactions :min="startDate" :max="endDateSnapped"/>
		</mdc-layout-cell>
	</mdc-layout-grid>
	</div>
</template>

<script>
  import Transactions from "@/components/Transactions";
  import moment from 'moment'


  export default {
	name: 'TransactionsPage',
	components: {
	  Transactions
	},
	data() {
	  return {
	    timeFrame: 'month',
		endDate: moment(),
		now: moment(),
		endDateSnapped: null,
		startDate: null
	  }
	},
	methods: {
	  onSelected(idx) {
		if (idx == 0){
		  this.timeFrame = 'week'
		}
		if (idx == 1){
		  this.timeFrame = 'month'
		}
		if (idx == 2){
		  this.timeFrame = 'year'
		}
		this.setEndDateSnapped()
		this.setStartDate()
	  },
	  addDate(){
		if (this.timeFrame == 'week'){
		  this.endDate.add('weeks', 1)
		}
		if (this.timeFrame == 'month'){
		  this.endDate.add('months', 1)
		}
		if (this.timeFrame == 'year'){
		  this.endDate.add('years', 1)
		}
		this.setEndDateSnapped()
		this.setStartDate()
	  },
	  subDate(){
		if (this.timeFrame == 'week'){
		  this.endDate.subtract('weeks', 1)
		}
		if (this.timeFrame == 'month'){
		  this.endDate.subtract('months', 1)
		}
		if (this.timeFrame == 'year'){
		  this.endDate.subtract('years', 1)
		}
		this.setEndDateSnapped()
		this.setStartDate()
	  },
	  setEndDateSnapped(){
		if (this.timeFrame == 'week'){
		  this.endDateSnapped = this.endDate.clone().day(7)
		}
		if (this.timeFrame == 'month'){
		  this.endDateSnapped = this.endDate.clone().add('months', 1).date(0)
		}
		if (this.timeFrame == 'year'){
		  this.endDateSnapped = this.endDate.clone().add('years', 1).month(0).date(0)
		}
	  },
	  setStartDate(){
	    if (this.timeFrame == 'week'){
	      this.startDate = moment(this.endDate).day(1)
		}
		if (this.timeFrame == 'month'){
		  this.startDate = moment(this.endDate).date(1)
		}
		if (this.timeFrame == 'year'){
		  this.startDate = moment(this.endDate).dayOfYear(1)
		}
	  }
	},
	created() {
	  this.setEndDateSnapped()
	  this.setStartDate()
	}
  }
</script>

<style scoped>

	.transactionsList {
		background: #373740;
		overflow: scroll;
		height: calc(100vh - 96px);
	}

	.dateSelect {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		margin-top: 5px;
	}

	.timeFrame {
		color: #AEAEB1;
		line-height: 20px;
		vertical-align: top;
		font-family: Roboto
	}

</style>
