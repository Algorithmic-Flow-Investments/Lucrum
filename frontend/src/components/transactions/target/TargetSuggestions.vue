<template>
	<div>
		<h1>Suggestions</h1>
		<h2>{{transaction.raw_info}}</h2>
		<h2>£{{transaction.amount}}</h2>
		<target-suggestion v-for="(suggestion,s) in suggestions" :suggestion="suggestion" :transaction="transaction" :key="s" @select="$emit('select', $event)" @selectEdit="$emit('selectEdit', $event)"></target-suggestion>
	</div>
</template>

<script>
	import Transaction from "@/Models/Transaction";
	import TargetSuggestion from "@/components/transactions/target/TargetSuggestion";
	import * as requests from "@/helpers/requests"

	export default {
		name: "TargetSuggestions",
		components: { TargetSuggestion },
		props: {transaction: Transaction},
		data() {
			return {
				suggestions: []
			}
		},
		created() {
			this.transaction.fetchTargetSuggestions().then(data => {
				this.suggestions = data
			})
		}
	};
</script>

<style scoped lang="scss">
	@import "../../../assets/colours";
	h1 {
		color: $text-strong;
		text-align: center;
	}

	h2 {
		text-align: center;
	}
</style>
