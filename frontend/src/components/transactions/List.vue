<template>
	<div ref="sect" class="sect">
		<transition-group name="slide-in" :style="{ '--total': transactionsLength }">
				<transaction
						:active-transaction="activeTransaction"
						:data="transaction"
						:key="transaction.id"
						:categories="categories"
						@activate="activeTransaction = $event; $emit('scroll', $event)"
						@deactivate="activeTransaction = null"
						@update-target="updateTarget"
						ref="transactions"
						v-for="(transaction, i) in transactions"
						:style="{'--i': i, '--reverse': (range.forward) ? 1 : -1}"
				></transaction>
		</transition-group>
	</div>
</template>

<script>
import * as requests from "@/helpers/requests";
import Transaction from "@/components/transactions/Transaction";
export default {
	name: "List",
	components: { Transaction },
	props: {
		range: Object,
		target_id: {
			type: Number,
			default: null
		},
		categories: {
			type: Array,
			default: () => {return []}
		}
	},
	data() {
		return {
			transactions: [],
			transactionsLength: 0,
			activeTransaction: null,
			topTransaction: null,
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
			requests
				.get("transactions/list", {
					params: {
						min: this.range.min.format("YYYY-M-D"),
						max: this.range.max.format("YYYY-M-D"),
						target_id: this.target_id
					}
				})
				.then(transactions => {
					this.transactions = transactions;
					this.transactionsLength = this.transactions.length
					this.topTransaction = this.transactions[0]
					this.$emit('scroll', this.topTransaction)
					this.$emit('loaded')
				});
		},
		updateTarget(updated) {
			if (this.target_id){
				this.transactions = this.transactions.filter(transaction => {
					return updated.indexOf(transaction.id) === -1;
				})
			}
			this.$refs.transactions
				.filter(comp => {
					return updated.indexOf(comp.data.id) !== -1;
				})
				.forEach(comp => {
					comp.fetch();
				});

			this.$emit('loaded')
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
		}
	},
	created() {
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
