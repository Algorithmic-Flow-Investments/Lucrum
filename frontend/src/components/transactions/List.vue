<template>
	<div ref="sect" class="sect">
		<transition-group name="slide-in" :style="{ '--total': transactions.length }">
				<TransactionSegment
						:active-transaction="activeTransaction"
						:transaction="transaction"
						:key="transaction.id"
						@activate="activeTransaction = $event; $emit('scroll', $event)"
						@deactivate="activeTransaction = null"
						ref="transactions"
						v-for="(transaction, i) in transactions"
						:style="{'--i': i, '--reverse': (range.forward) ? 1 : -1}"
				></TransactionSegment>
		</transition-group>
	</div>
</template>

<script>
import * as requests from "@/helpers/requests";
import TransactionSegment from "@/components/transactions/TransactionSegment";
import Transaction from "@/Models/Transaction";
export default {
	name: "List",
	components: { TransactionSegment },
	props: {
		range: Object,
		extra_params: {
			type: Object,
			default: () => {return {}}
		}
	},
	data() {
		return {
			transactions: [],
			activeTransaction: null,
			topTransaction: null
		};
	},
	/*watch: {
		"range.min": function() {
			this.fetch();
		},
		"range.max": function() {
			this.fetch();
		}
	},*/
	methods: {
		fetch() {
			if (this.range.min === null || this.range.max === null) return;
			this.transactions = []
			let params = {
				min: this.range.min.format("YYYY-M-D"),
				max: this.range.max.format("YYYY-M-D"),
			}
			params = Object.assign(params, this.extra_params)
			requests
				.get("transactions/list", {
					params: params
				})
				.then(transactions => {
					this.transactions = transactions.map(t => new Transaction(t));
					this.topTransaction = this.transactions[0]
					this.joinTransactionsTargets()
					this.joinTransactionsMethods()
					this.joinTransactionsAccounts()
					this.$emit('scroll', this.topTransaction)
					this.$emit('loaded')
				});
		},
		joinTransactionsTargets(transactions) {
			if (this.l_targets.length > 0 && transactions) {
				transactions.forEach(transaction => transaction.target = transaction.getTarget())
			}
		},
		joinTransactionsMethods() {
			if (this.l_methods.length > 0 && this.transactions) {
				this.transactions.forEach(transaction => transaction.method = transaction.getMethod())
			}
		},
		joinTransactionsAccounts() {
			if (this.l_accounts.length > 0 && this.transactions) {
				this.transactions.forEach(transaction => transaction.account = transaction.getAccount())
			}
		},
		joinTransactionsTags() {
			if (this.l_tags.length > 0 && this.transactions) {
				this.transactions.forEach(transaction => transaction.tags = transaction.getTags())
			}
		},
		handleScroll() {
			if (this.activeTransaction){
				this.topTransaction = this.activeTransaction
				this.$emit('scroll', this.topTransaction)
				return
			}
			let top = this.$refs.transactions.find(comp => {
				if (comp.hidden) return false;
				let dist = comp.$el.getBoundingClientRect().top - this.$refs.sect.getBoundingClientRect().top
				return dist > 0 && dist < 60;
			})
			if (top){
				this.topTransaction = top.transaction
				this.$emit('scroll', this.topTransaction)
			}
		},
		onTransactionsUpdated(transaction_ids) {
			let transactions = this.transactions.filter(transaction => transaction_ids.includes(transaction.id))
			transactions.forEach(transaction => {
				transaction.fetch()
			})
			this.joinTransactionsTargets(transactions)
		},
		onTargetsUpdated(target_ids) {
			this.$store.dispatch('fetch_targets').then(() => this.joinTransactionsTargets(this.transactions))
		}
	},
	created() {
		this.$store.dispatch('fetch_targets').then(() => this.joinTransactionsTargets(this.transactions))
		this.$store.dispatch('fetch_methods').then(() => this.joinTransactionsMethods())
		this.$store.dispatch('fetch_accounts').then(() => this.joinTransactionsAccounts())
		this.$store.dispatch('fetch_tags').then(() => this.joinTransactionsTags())
		this.$store.dispatch('fetch_categories')
		this.fetch();
	},
	mounted() {
		this.$el.addEventListener('scroll', this.handleScroll);
	},
	destroyed () {
		this.$el.removeEventListener('scroll', this.handleScroll);
	}
};
</script>

<style scoped lang="scss">
.sect {
	height: calc(100vh - 24px);
	overflow-y: scroll;
	padding-top: 10px;
}

.slide-in {
	$total-length: 1s;
	$proportion: calc(1 - var(--i) / var(--total));
	$length: calc(#{$total-length} * #{$proportion});
	$delay: calc(#{$total-length} * (1 - #{$proportion}));

	&-move {
		 transition: opacity $length linear, transform $length ease-in-out !important;
	 }

	&-leave-active {
		 transition: opacity $length linear, transform $length cubic-bezier(.5,0,.7,.4) !important; //cubic-bezier(.7,0,.7,1);
		 transition-delay: $delay !important;
	 }

	&-enter-active {
		 transition: opacity $length linear, transform $length cubic-bezier(.2,.5,.1,1) !important;
		 transition-delay: $delay !important;
	 }

	&-enter,
	&-leave-to {
		 opacity: 0;
	 }

	&-enter { transform: translateX(calc(100% * var(--reverse))); }
	&-leave-to { transform: translateX(calc(-110% * var(--reverse))); }

}


</style>
