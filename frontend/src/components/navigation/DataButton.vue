<template>
	<div class="nav-button" @click="popup=!popup">
		<b-icon icon="server" size="is-medium" />
		<span class="name">{{stats.transactions}} total</span>
		<span class="name">{{latest_update}}</span>
		<div v-if="popup" class="popup">
			<b-button type="is-danger" @click="rebuild">Rebuild and populate</b-button>
			<b-button type="is-primary" @click="populate">Populate</b-button>
			<b-button type="is-primary" @click="update">Update</b-button>
		</div>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests"
	import moment from "moment"
	import BButton from "buefy/src/components/button/Button";

	export default {
		name: "DataButton",
		components: { BButton },
		data () {
			return {
				stats: {},
				popup: false
			}
		},
		methods: {
			fetch() {
				requests.get('meta/stats').then(data => {
					this.stats = data
				})
			},
			rebuild() {
				requests.post('meta/rebuild').then(data => {
					location.reload();
				})
			},
			populate() {
				requests.post('meta/populate').then(data => {
					location.reload();
				})
			},
			update() {
				requests.post('meta/update').then(data => {
					location.reload();
				})
			}
		},
		computed: {
			latest_update() {
				return moment(this.stats.latest).format('DD/MM/YYYY')
			}
		},
		created() {
			this.fetch()
		}
	};
</script>

<style scoped>
	.nav-button {
		display: inline-block;
		width: 100%;
		cursor: pointer;
		padding-top: 42px;
		text-align: center;
		position: absolute;
		bottom: 0;
		left: 0;
	}

	.name {
		font-family: "Roboto Condensed", serif;
		color: white;
		display: block;
	}

	@media screen and (max-width: 768px) {
		.nav-button {
			width: fit-content;
		}

		.name {
			display: inline-block;
		}
	}

	.popup {
		background-color: rgba(0, 0, 0, 0.5);
		position: fixed;
		bottom: 140px;
		left: 40px;
		padding: 10px;
	}

	.popup::after {
		content: " ";
		position: absolute;
		top: 100%; /* At the bottom of the tooltip */
		left: 5px;
		margin-left: -5px;
		border-width: 20px;
		border-style: solid;
		border-color: black transparent transparent transparent;
	}

	.popup button {
		display: block;
		margin: 5px;
	}

</style>
