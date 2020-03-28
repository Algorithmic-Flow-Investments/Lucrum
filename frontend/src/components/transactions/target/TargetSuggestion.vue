<template>
	<div class="suggestion" :class="suggestion.reason.type">
		<span class="info">
			<span class="target-name">{{target_name}}</span>
			<span class="reason">Reason: {{suggestion.reason.type}}</span>
			<span class="transaction" v-if="linkedTransaction">
				<span>Transaction amount: {{linkedTransaction.amount}}</span>
				<span>Transaction time difference: {{time_difference}} days</span>
			</span>
			<span class="word" v-if="suggestion.reason.word">Matched word: {{suggestion.reason.word}}</span>
		</span>
		<b-button type="button" size="is-small" @click="$emit('select', target)">Select</b-button>
		<b-button type="button" size="is-small" @click="$emit('selectEdit', target)">Select & Edit</b-button>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests"
	import Transaction from "@/Models/Transaction";
	export default {
		name: "TargetSuggestion",
		props: ["suggestion", "transaction"],
		data() {
			return {
				target: null,
				linkedTransaction: null
			}
		},
		methods:{
			fetchTransaction() {
				if (!this.suggestion.reason.transaction_id) {
					return
				}
				requests.get(`transactions/get/${this.suggestion.reason.transaction_id}`).then(data => {
					this.linkedTransaction = new Transaction(data)
				})
			}
		},
		computed: {
			target_name() {
				return (this.target) ? this.target.name : "";
			},
			time_difference() {
				return this.transaction.date.diff(this.linkedTransaction.date, 'days', true)
			}
		},
		created() {
			this.target = this.l_targets.filter(t => t.id === this.suggestion.target_id)[0]
			this.fetchTransaction()
		}
	};
</script>

<style scoped lang="scss">
	@import "../../../assets/colours";

	.target-name {
		color: $text-strong;
	}

	.suggestion {
		border-width: 2px;
		border-style: solid;
		padding: 4px;
		/*display: flex;*/
		/*justify-content: space-between;*/
	}

	.matched_word {
		border-color: $blue;
	}

	.nearby_transaction {
		border-color: $secondary;
	}

	.suggestion span {
		margin-right: 10px;
	}

	/deep/ .button {
		width: initial !important;
		margin-top: initial !important;
	}

</style>
