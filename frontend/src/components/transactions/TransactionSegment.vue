<template>
	<segment :colour="colour"
			 :amount="transaction.amount"
			 :title="target_name.concat((isInBudget) ? '' : ' N')"
			 :subtitle="date"
			 @activate="$emit('activate', transaction)"
			 @deactivate="$emit('deactivate')"
			 ref="segment"
			 v-show="!hidden"
			 :internal="is_internal">
		<transaction-edit :transaction="transaction"></transaction-edit>
	</segment>
</template>

<script>
import Segment from "@/components/Segment";
import moment from "moment";
import TransactionEdit from "@/components/transactions/TransactionEdit";
import * as requests from "@/helpers/requests";
import Transaction from "@/Models/Transaction";

export default {
	name: "TransactionSegment",
	components: { TransactionEdit, Segment },
	props: {
		transaction: Transaction,
		activeTransaction: Object,
		categories: Array,
	},
	data() {
		return {
			active: false
		};
	},
	watch: {
		activeTransaction() {
			if (this.activeTransaction && this.activeTransaction.id !== this.transaction.id && !this.hidden){
				this.$refs.segment.active = false
			}
		}
	},
	methods: {
		fetch() {
			requests.get(`transaction/${this.transaction.id}`).then(data => {
				this.transaction = data
			})
		}
	},
	computed: {
		colour() {
			if (this.is_internal) {
				return "internal"
			}
			if (this.transaction.amount > 0) {
				return "positive"
			}
			if (this.transaction.amount < 0) {
				return "negative"
			}
			return "null"
		},
		target_name() {
			if (!this.transaction.target) return this.transaction.raw_info;
			if (this.is_internal) {
				if (this.transaction.amount < 0) {
					return this.transaction.account.name + " -> " + this.transaction.target.name
				}
				else {
					return this.transaction.target.name + " -> " + this.transaction.account.name
				}
			}
			return this.transaction.target.name;
		},
		date() {
			return moment(this.transaction.date).format("ddd, D MMM YYYY");
		},
		is_internal() {
			return this.transaction.target && this.transaction.target.is_internal
		},
		hidden() {
			if (this.internal){
				if (this.transaction.amount > 0){
					return true
				}
			}
			return false
		},
		isInBudget(){
			return true;
			return this.transaction.tags.filter(tag => tag.category && this.categories.indexOf(tag.category.id) !== -1).length > 0
		}
	}
};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";

	/deep/ .positive {
		background-color: $yellow;
	}

	/deep/ .negative {
		background-color: $red;
	}

	/deep/ .internal {
		background-color: $blue;
	}
</style>
