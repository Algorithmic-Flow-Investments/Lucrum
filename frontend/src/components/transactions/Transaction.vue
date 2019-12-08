<template>
	<segment :colour="colour"
			 :amount="transaction.amount"
			 :title="target.concat((isInBudget) ? '' : ' N')"
			 :subtitle="date"
			 @activate="$emit('activate', transaction)"
			 @deactivate="$emit('deactivate')"
			 ref="segment"
			 v-show="!hidden"
			 :internal="internal">
		<transaction-edit :data="transaction" @update-target="$emit('update-target', $event)"></transaction-edit>
	</segment>
</template>

<script>
import Segment from "@/components/Segment";
import moment from "moment";
import TransactionEdit from "@/components/transactions/TransactionEdit";
import * as requests from "@/helpers/requests";

export default {
	name: "Transaction",
	components: { TransactionEdit, Segment },
	props: ["data", "activeTransaction", "categories"],
	data() {
		return {
			transaction: this.data,
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
			if (this.internal) {
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
		target() {
			return ((!this.transaction.target) ? this.transaction.raw :
				   (this.internal) ? this.transaction.account.name + " -> " + this.transaction.target.name : this.transaction.target.name);
		},
		date() {
			return moment(this.transaction.date).format("ddd, D MMM YYYY");
		},
		internal() {
			return this.transaction.target && this.transaction.target.internal
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
