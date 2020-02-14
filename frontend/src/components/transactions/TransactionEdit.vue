<template>
<div class="transaction-edit">
	<div class="raw">{{ transaction.raw_info }}</div>
	<div class="edit target" @click.stop="editTarget=true"><i class="fas fa-bullseye"></i>
		<span v-if="transaction.target">{{ transaction.target.name }}</span>
		<span v-else style="display: flex;">Select Target</span>
	</div>
	<div class="edit method"><i class="fas fa-cash-register"></i>
		<span v-if="transaction.method">{{ transaction.method.name }}</span>
		<span v-else style="display: flex;">Select Method</span>
	</div>
	<div class="edit account"><i class="fas fa-university"></i>
		<span>{{ transaction.account.name }}</span>
	</div>

	<div class="timeline">
		<span><a :href="timeline_link" target="_blank">Timeline</a> </span>
	</div>

	<div class="edit">Tags</div>

	<b-modal :active.sync="editTarget" has-modal-card>
		<transaction-target :transaction="transaction" @close="editTarget=false"></transaction-target>
	</b-modal>
</div>
</template>

<script>
	import TransactionTarget from "@/components/transactions/TransactionTarget";
	import Transaction from "@/Models/Transaction";
	export default {
		name: "TransactionEdit",
		components: { TransactionTarget },
		props: {
			transaction: Transaction
		},
		data() {
			return {
				editTarget: false
			}
		},
		computed: {
			timeline_link() {
				let date = this.transaction.date.format('Y-M-D')
				return `https://www.google.com/maps/timeline?pb=!1m2!1m1!1s${date}`
			}
		}
	};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";

	.raw {
		color: $text-strong;
		font-size: 14px;
		width: fit-content;
		margin: auto;
	}

	.edit {
		display: flex;
		padding-bottom: 8px;
	}

	.edit span {
		margin-left: 2px;
	}

	.target {
		font-size: 28px;
		line-height: 28px;
	}

	/*.transaction-edit {
		font-size: 22px;
		line-height: 24px;
	}*/

</style>
