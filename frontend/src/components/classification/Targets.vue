<template>
	<div class="sect">
		<target v-for="target in targets" :key="target.id" :target="target" :tags="tags" @delete="del(target)"/>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests";
	import Target from "@/components/classification/Target";

	export default {
		name: "Targets",
		components: { Target },
		data () {
			return {
				targets: [],
				tags: []
			}
		},
		methods: {
			fetch() {
				requests.get('targets/list').then(targets => {
					this.targets = targets.filter(target => {
						return !target.internal
					}).sort((a, b) => a.tags.length - b.tags.length)
				})
				requests.get('tags/list').then(tags => {
					this.tags = tags
				})
			},
			del(target) {
				requests.del(`target/${target.id}/delete`).then(() => {
					this.targets.splice(this.targets.indexOf(target), 1)
				})
			}
		},
		created() {
			this.fetch()
		}
	};
</script>

<style scoped>

	.sect {
		padding-top: 10px;
	}

</style>
