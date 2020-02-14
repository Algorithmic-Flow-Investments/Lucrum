<template>
	<div style="cursor: pointer" @click="toggle">
		<span class="fa-stack fa-1x">
		  <i class="far fa-circle fa-stack-2x"></i>
		  <i class="fa fa-wave-square fa-stack-1x"></i>
		</span>
	</div>
</template>

<script>
	export default {
		name: "TotalTypeToggle",
		data() {
			return {
				totalType: this.$route.query.total_type || 'outgoing'
			}
		},
		methods: {
			toggle() {
				switch (this.totalType) {
					case 'outgoing':
						this.totalType = 'gross';
						break;
					case 'gross':
						this.totalType = 'income';
						break;
					case 'income':
						this.totalType = 'outgoing';
						break;
				}
				this.update()
			},
			update() {
				this.$router.push({ query: Object.assign({}, this.$route.query, {total_type: this.totalType})})
				this.$emit('changed', this.totalType)
			}
		},
		created() {
			this.update()
		}
	};
</script>

<style scoped>
</style>
