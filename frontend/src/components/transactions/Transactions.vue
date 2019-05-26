<template>
	<div class="transactions" ref="transactions">
		<transaction-segment
			v-for="transaction in transactions"
			:ref="transaction.id"
			:key="transaction.id"
			:data="transaction"
			@update="updateData()"
			@link="link=$event"
			:link="link"
		/>
	</div>
</template>

<script>
import TransactionSegment from "@/components/transactions/TransactionSegment";
import axios from "axios/index";
import VueScrollTo from "vue-scrollto";

import { EventBus } from "../../event-bus.js";

export default {
	name: "Transactions",
	props: ["min", "max"],
	components: {
		TransactionSegment
	},
	data() {
		return {
			transactions: [],
			textTruncateLength: 16,
			fetching: false,
			fetchNum: 0,
			link: null
		};
	},
	watch: {
		min: function() {
			this.fetchData();
		},
		max: function() {
			this.fetchData();
		}
	},
	methods: {
		fetchData() {
			if (this.min == null || this.max == null) return;
			let fetchNum = ++this.fetchNum;
			this.fetching = true
			axios
				.get(window.APIROOT + "api/transactions/list", {
					params: {
						min: this.min.format("YYYY-M-D"),
						max: this.max.format("YYYY-M-D")
					}
				})
				.then(response => {
					if (fetchNum === this.fetchNum){
						console.log("fetchData")
						this.transactions = response.data;
						this.fetching = false
					}
				});
		},
		updateData() {
			if (this.min == null || this.max == null || this.fetching) return;
			this.fetching = true
			axios
				.get(window.APIROOT + "api/transactions/list", {
					params: {
						min: this.min.format("YYYY-M-D"),
						max: this.max.format("YYYY-M-D")
					}
				})
				.then(response => {
					let transactions = response.data;
					for (let t in transactions) {
						for (let key in transactions[t]){
							this.$set(this.transactions[t], key, transactions[t][key])
						}
					}
					this.fetching = false
				});
		},
		handleResize() {
			this.textTruncateLength = 16 + 3 * ((window.innerWidth - 320) / 1600);
		}
	},
	created() {
		this.fetchData();
		window.addEventListener("resize", this.handleResize);
		this.handleResize();
		//setTimeout(this.updateData, 2000)
	},
	destroyed() {
		window.removeEventListener("resize", this.handleResize);
	}
};
</script>

<style scoped></style>
