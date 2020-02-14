<template>
	<target-select v-if="state === 'select'"
				   :transaction="transaction"
				   :saving="saving"
				   @new="newTarget"
				   @close="close"></target-select>
	<target-edit v-else-if="state === 'edit'"
				 :transaction="transaction"
				 :saving="saving"
				 @close="close">
	</target-edit>
</template>

<script>
	import TargetSelect from "@/components/transactions/target/TargetSelect";
	import * as requests from "@/helpers/requests"
	import TargetEdit from "@/components/transactions/target/TargetEdit";

	export default {
		name: "TransactionTarget",
		components: { TargetEdit, TargetSelect },
		props: ['transaction'],
		data() {
			return {
				state: (this.transaction.target) ? 'edit' : 'select',
				selectedTarget: '',
				saving: false
			}
		},
		methods: {
			newTarget() {
				this.state = 'edit'
			},
			// editTarget(target){
			// 	this.saving = true
			// 	requests.post(`target/${target.id}/edit`, target).then(target_data => {
			// 		requests.post(`transaction/${this.transaction.id}`, {
			// 			target: target_data.target.id
			// 		}).then(data =>{
			// 			this.transaction.target = data.target;
			// 			this.$emit('update', target_data.updated)
			// 			this.$notification.open({
			// 				message: `Updated ${target_data.updated.length} transactions`,
			// 				type: 'is-success'
			// 			})
			// 			this.$parent.close()
			// 		})
			// 	}).catch(exception => {
			// 		this.saving = false
			// 		this.$dialog.alert({
			// 			title: 'Error',
			// 			message: 'A target with this name already exists',
			// 			type: 'is-danger',
			// 			hasIcon: true,
			// 			icon: 'times-circle',
			// 			iconPack: 'fa'
			// 		})
			// 	})
			// },
			close() {
				this.$emit('close')
			}
		}
	};
</script>

<style scoped>

</style>
