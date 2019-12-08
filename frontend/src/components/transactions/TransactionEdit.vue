<template>
<div class="transaction-edit">
	<div class="raw">{{ data.raw }}</div>
	<div class="edit target" @click.stop="editTarget=true"><i class="fas fa-bullseye"></i>
		<span v-if="data.target">{{ data.target.name }}</span>
		<span v-else style="display: flex;">Select Target</span>
	</div>
	<div class="edit method"><i class="fas fa-cash-register"></i>
		<span v-if="data.method">{{ data.method.name }}</span>
		<span v-else style="display: flex;">Select Method</span>
	</div>
	<div class="edit">Tags</div>

	<b-modal :active.sync="editTarget" has-modal-card>
		<transaction-target :transaction="data" @update="$emit('update-target', $event)"></transaction-target>
	</b-modal>
</div>
</template>

<script>
	import TransactionTarget from "@/components/transactions/TransactionTarget";
	export default {
		name: "TransactionEdit",
		components: { TransactionTarget },
		props: ['data'],
		data() {
			return {
				editTarget: false
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
