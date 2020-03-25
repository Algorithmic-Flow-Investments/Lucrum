<template>
	<div class="transaction-extra">
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
<!--		<div class="edit date"><i class="fas fa-clock"></i>-->
<!--			<span>{{ transaction.date }}</span>-->
<!--		</div>-->

		<transaction-edit-field icon="fa-clock" :value="transaction.date" :extra="transaction.extra.date"></transaction-edit-field>

		<div class="timeline">
			<span><a :href="timeline_link" target="_blank">Timeline</a> </span>
		</div>

		<div class="edit">Tags</div>
		<b-taglist>
			<b-tag v-for="tag in transaction.tags" :key="tag.id" type="is-primary">{{tag.name}}</b-tag>
		</b-taglist>

		<b-modal :active.sync="editTarget" has-modal-card>
			<transaction-target :transaction="transaction" @close="editTarget=false"></transaction-target>
		</b-modal>
	</div>
</template>

<script>
	import TransactionTarget from "@/components/transactions/TransactionTarget";
	import Transaction from "@/Models/Transaction";
	import TransactionEditField from "@/components/transactions/TransactionEditField";
	export default {
		name: "TransactionExtra",
		components: { TransactionEditField, TransactionTarget },
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
		},
		created() {
			this.transaction.fetch()
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
		padding-bottom: 5px;
	}

	.edit {
		display: flex;
		padding-bottom: 10px;
		cursor: pointer;
	}

	.edit span {
		margin-left: 2px;
	}

	.edit i {
		line-height: inherit;
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
