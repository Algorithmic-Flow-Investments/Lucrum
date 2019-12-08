<template>
	<!--b-loading :is-full-page="false" :active.sync="isLoading"></b-loading-->
	<div v-if="isLoading">
		<div style="color: #63c5ab" class="la-ball-spin-clockwise">
			<div></div>
			<div></div>
			<div></div>
			<div></div>
			<div></div>
			<div></div>
			<div></div>
			<div></div>
		</div>
	</div>
</template>

<script>
	import {EventBus} from "@/helpers/requests";

	export default {
		name: "Loading",
		data() {
			return {
				sending: 0,
				deleting: 0
			}
		},
		computed: {
			isLoading() {
				return this.sending + this.deleting > 0
			}
		},
		created() {
			EventBus.$on('sending', () => this.sending++)
			EventBus.$on('sent', () => this.sending--)

			EventBus.$on('deleting', () => this.deleting++)
			EventBus.$on('deleted', () => this.deleting--)
		}
	};
</script>

<style scoped>
	@import '~load-awesome/css/ball-spin-clockwise.min.css';

	.la-ball-spin-clockwise {
		position: fixed;
		right: 10px;
		bottom: 10px;
		z-index: 1000;
	}

</style>
