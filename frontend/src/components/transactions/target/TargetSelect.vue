<template>
	<div class="modal-card" style="width: auto">
		<header class="modal-card-head">
			<p class="modal-card-title">Select Target</p>
		</header>
		<section class="modal-card-body">
			<div v-if="transaction.target === null">
				<multiselect v-model="selectedTarget" :options="l_targets" label="name" placeholder="Select target">
					<template slot="option" slot-scope="props">
						<i v-if="props.option.is_internal" class="fas fa-university"></i>
						<span class="option__title">{{ props.option.name }}</span>
					</template>
				</multiselect>
				<b-button @click="$emit('new')">Create new</b-button>
			</div>
		</section>
		<footer class="modal-card-foot">
			<b-button type="button" @click="$emit('close')">Close</b-button>
			<b-button type="is-primary" @click="save()" :disabled="selectedTarget === null" :loading="saving">Save</b-button>
			<b-button type="is-primary" @click="saveEdit()" :disabled="selectedTarget === null" :loading="saving">Save & Edit</b-button>
		</footer>
	</div>
</template>

<script>
	import Multiselect from 'vue-multiselect'

	export default {
		name: "TargetSelect",
		components: { Multiselect },
		props: ['transaction'],
		data() {
			return {
				selectedTarget: null,
				saving: false
			}
		},
		methods: {
			save() {
				this.transaction.target_id = this.selectedTarget.id
				this.transaction.manual_target = true
				this.transaction.commit().finally(() => {
					this.saving = false;
					this.$emit('close')
				})
			},
			saveEdit() {
				this.transaction.target_id = this.selectedTarget.id
				this.transaction.manual_target = true
				this.transaction.commit().finally(() => {
					this.saving = false;
					this.$emit('close-edit')
				})
			}
		}
	};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped lang="css">

	.modal-card-body {
		min-width: 50vw;
		min-height: 20vh;
		overflow: visible;
	}

	.modal-card {
		overflow: visible;
	}

	.svg-inline--fa {
		margin-right: 2px;
	}

	.modal-card-foot {
		justify-content: flex-end
	}

	/deep/ .button {
		margin-top: 5px;
		width: 100%;
	}

</style>
