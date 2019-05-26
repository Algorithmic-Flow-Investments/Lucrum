<template>
	<div>
		<mdc-dialog :open="open" @cancel="$emit('close', $event)" @accept="apply" :title="(id === -1) ? 'Select Target' : 'Edit Target'" accept="Apply" cancel="Cancel">
			<template v-if="id === -1 && selected !== 'new'">
				<multiselect v-model="selected" :options="targets" placeholder="Select a target" label="name" track-by="name"></multiselect>
				<div style="text-align: center; margin-top: 10px">or</div>
				<mdc-button raised @click="selected = 'new'" style="margin-top: 10px; width: 100%; position: relative">New Target</mdc-button>
			</template>
			<template v-else>
				<edit-inputs v-if="true" v-model="data" :predicted="predicted"></edit-inputs>
				<mdc-button id="et_unlink" v-if="selected !== 'new'" raised @click="unlink()">Unlink</mdc-button>
				<mdc-button id="et_delete" v-if="selected !== 'new'" raised @click="remove()">Delete</mdc-button>
			</template>
		</mdc-dialog>
	</div>
</template>

<script>
import EditInputs from "@/components/transactions/EditInputs";
import Multiselect from "vue-multiselect";


import axios from "axios";

export default {
	name: "EditTarget",
	components: { EditInputs, Multiselect },
	props: ['id', 'predicted', 'parent'],
	data() {
		return {
			data: {
				name: "",
				strings: []
			},
			loaded: false,
			targets: [],
			selected: null,
			open: false,
			edit: false
		};
	},
	methods: {
		close() {
			this.$router.push({ params: { edit: null } });
		},
		fetchData() {
			if (this.id === -1){
				axios.get(window.APIROOT + "api/targets").then(response => {
					this.targets = response.data;
					this.targets.forEach(target => {
						if (target.internal){
							target.name += " (internal)"
						}
					})
				});
			}
			else {
				axios.get(window.APIROOT + "api/target/" + this.id).then(response => {
					let data = response.data;
					this.data.name = data.name;
					this.data.strings = data.strings;
				});
			}
		},

		remove() {
			// TODO: Warning before deletion (how many transactions will be effected)
			axios.delete(window.APIROOT + `api/target/${this.id}`).then(response => {
				this.$emit("close");
				this.$emit("update");
			});
		},

		unlink() {
			axios.post(window.APIROOT + `api/transaction/${this.$route.params.transactionId}`, { target: null }).then(response => {
				this.$emit("close");
				this.$emit("update");
			});
		},

		submit() {
			axios.post(window.APIROOT + `api/target/${this.id}`, { name: this.data.name, strings: this.data.strings }).then(response => {
				if (response.data === "EXISTS") {
					this.$emit("close");
					alert("Target name exists"); // TODO: Create proper popup
				} else {
					let id = response.data.id;
					axios.post(window.APIROOT + `api/transaction/${this.parent}`, { target: id }).then(response => {
						this.$emit("update");
						this.$emit("close");
					});
				}
			});
		},

		select() {
			axios.post(window.APIROOT + `api/transaction/${this.parent}`, { target: this.selected.id }).then(response => {
				this.$emit("update");
				this.$emit("close");
			});
		},
		apply() {
			if (this.id === -1 && this.selected !== 'new'){
				this.select()
			}
			else {
				this.submit()
			}
		}
	},
	created() {
		this.fetchData();
	},
	mounted() {
		this.$nextTick(() => {
			this.open = true
		})
	},
	beforeDestroy() {
		this.open = false
	}
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>


<style>
.mdc-button--raised {
	background-color: #007d51 !important;
	width: 49%;
	margin-top: 24px;
}

	.mdc-dialog .mdc-dialog__header {
		color: rgb(255, 255, 255)
	}

.mdc-dialog .mdc-dialog__body {
	color: rgba(255, 255, 255, 0.54)
}
</style>

<style scoped>
	.multiselect {
		width: 100%;
	}
</style>
