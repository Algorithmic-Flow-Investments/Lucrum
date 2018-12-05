<template>
<div>
	<multiselect v-model="selected" :options="methods" placeholder="Select a method" label="name" track-by="name"></multiselect>
	<mdc-button raised @click="selected = 'new'">New Target</mdc-button>
</div>
</template>

<script>
	import Multiselect from 'vue-multiselect'
	import { EventBus } from '../event-bus.js';
	import axios from "axios";


	export default {
		name: 'SelectTarget',
		components: { Multiselect },
		data () {
		  return {
			methods: [],
			selected: null
		  }
		},
		watch: {
		  selected: function(){
			if (this.selected === "new"){
				this.$emit('new')
			}
			else if (this.selected){
			  axios.post(window.APIROOT + `api/transaction/${this.$route.params.transactionId}`,
				{method: this.selected.id}
			  ).then(response => {
				this.$emit('close')
			  })
			}
		  }
		},
		methods: {
		  fetchData() {
			axios.get(window.APIROOT + "api/methods").then(response => {
			  this.methods = response.data;
			})
		  },
		},
		created() {
		  this.fetchData()
		}
	}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>


<style>
	.mdc-button--raised {
		position: absolute;
		background-color: #007d51 !important;
		left: 5%;
		margin-top: 10px;
		width: 90%;
	}
</style>

<style scoped>

	.multiselect {
		width: 90%;
		margin-left: 5%;
		margin-top: 50%;
	}



</style>
