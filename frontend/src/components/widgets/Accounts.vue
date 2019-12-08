<template>
	<proportional-list title="Accounts" subtitle="£1234" :items="items"></proportional-list>
</template>

<script>
	import ProportionalList from "@/components/widgets/ProportionalList";
	import * as requests from "@/helpers/requests"
	export default {
		name: "Accounts",
		data () {
			return {
				items: []
			}
		},
		components: { ProportionalList },
		methods: {
			fetch() {
				requests.get('accounts/list').then(data => {
					this.items = data
				})
			}
		},
		created() {
			this.fetch()
		}
	};
</script>

<style scoped>

</style>
