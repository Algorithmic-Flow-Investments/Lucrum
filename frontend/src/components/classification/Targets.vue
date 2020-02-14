<template>
	<div class="sect">
		<target v-if="!target.is_internal" v-for="target in sorted_targets" :key="target.id" :target="target"  @delete="del(target)"/>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests";
	import Target from "@/components/classification/Target";

	export default {
		name: "Targets",
		components: { Target },
		data() {
			return {
				sorted_targets: []
			}
		},
		methods: {
			del(target) {
				requests.del(`targets/delete/${target.id}`).then(() => {
					this.l_targets.splice(this.l_targets.indexOf(target), 1)
				})
			}
		},
		watch: {
			l_targets() {
				this.sorted_targets = [...this.l_targets].sort((a, b) => {
					return a.tag_ids.length - b.tag_ids.length || b.usages - a.usages
				})
			}
		}
	};
</script>

<style scoped>

	.sect {
		padding-top: 10px;
	}

</style>
