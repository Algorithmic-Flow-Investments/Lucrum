<template>
	<div ref="transactions">
		<transaction-segment v-for="transaction in transactions" :ref="transaction.id" :key="transactions.indexOf(transaction)" :tid="transaction.id" :amount="transaction.amount" :tags="transaction.tags" :date="transaction.date" :target="transaction.target"/>
	</div>
</template>

<script>
  import TransactionSegment from "@/components/TransactionSegment";
  import axios from "axios";
  import VueScrollTo from 'vue-scrollto';

  import { EventBus } from '../event-bus.js';


  export default {
	name: 'Transactions',
	props: ['min', 'max'],
	components: {
	  TransactionSegment
	},
	data () {
	  return {
	    transactions: []
	  }
	},
	watch: {
	  min: function(){this.fetchData()},
	  max: function(){this.fetchData()},
	},
	methods: {
	  fetchData() {
		axios.get(window.APIROOT + "api/transactions", {
		  params: {
			min: this.min.format("YYYY-M-D"),
			max: this.max.format("YYYY-M-D")
		  }
		}).then(response => {
		  this.transactions = response.data;
		});
	  }
	},
	created() {
	  this.fetchData();
	  EventBus.$on('edit/close', () => {
	    this.fetchData()
	  })
	}
  }
</script>

<style scoped>

</style>
