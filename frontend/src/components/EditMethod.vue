<template>
	<div>
		<edit-inputs v-if="true" v-model="data" :predicted="predicted"></edit-inputs>
		<mdc-button id="et_unlink" v-if="id != -1" raised @click="unlink()">Unlink</mdc-button>
		<mdc-button id="et_delete" v-if="id != -1" raised @click="remove()">Delete</mdc-button>
		<mdc-button id="et_save" raised @click="submit()">Save</mdc-button>
	</div>
</template>

<script>
import { EventBus } from "../event-bus.js";
import EditInputs from "@/components/EditInputs";

import axios from "axios";

export default {
	name: "EditMethod",
	components: { EditInputs },
	data() {
		return {
			data: {
				name: "",
				strings: []
			},
			loaded: false,
			id: -1,
			predicted: ""
		};
	},
	methods: {
		close() {
			this.$router.push({ params: { edit: null } });
		},
		fetchData() {
			let parent = this.$route.params.transactionId;
			axios.get(window.APIROOT + "api/transaction/" + parent).then(response => {
				this.id = response.data.method ? response.data.method.id : "-1";
				this.predicted = response.data.raw;
				axios.get(window.APIROOT + "api/method/" + this.id).then(response => {
					let data = response.data;
					this.data.name = data.name;
					this.data.strings = data.strings;
					//this.loaded = true
				});
			});
		},

		remove() {
			// TODO: Warning before deletion (how many transactions will be effected
			axios.delete(window.APIROOT + `api/method/${this.id}`).then(response => {
				this.$emit("close");
			});
		},

		unlink() {
			axios.post(window.APIROOT + `api/transaction/${this.$route.params.transactionId}`, { method: null }).then(response => {
				this.$emit("close");
			});
		},

		submit() {
			axios.post(window.APIROOT + `api/method/${this.id}`, { name: this.data.name, strings: this.data.strings }).then(response => {
				if (response.data === "EXISTS") {
					alert("Method name exists"); // TODO: Create proper popup
				} else {
					this.id = response.data.id;
					axios.post(window.APIROOT + `api/transaction/${this.$route.params.transactionId}`, { method: this.id }).then(response => {
						this.$emit("close");
					});
				}
			});
		}
	},
	created() {
		this.fetchData();
	}
};
</script>

<style>
.mdc-button--raised {
	position: absolute;
	background-color: #007d51 !important;
}

#et_save {
	bottom: 10px;
	left: 50%;
	width: 90%;
	transform: translateX(-50%);
}

#et_unlink {
	bottom: 60px;
	left: 5%;
	width: 42.5%;
}

#et_delete {
	bottom: 60px;
	left: 52.5%;
	width: 42.5%;
}
</style>

<style scoped></style>
