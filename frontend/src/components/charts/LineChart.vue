<template>
	<div class="chart">
		<div class="segment" v-for="(segment, i) in data" :class="segment[1]" :style="{ width: segment[0] + '%' }" :key="i"></div>
	</div>
</template>

<script>
export default {
	name: "LineChart",
	props: ["data"]
};
</script>

<style scoped>
.segment {
	height: 2px;
	display: inline-block;
}
.chart {
	display: flex;
	width: calc(100% + 40px);
	transform: translate(-20px);
	padding: 10px 0 10px 0;
}

@media (max-width: 479px) {
	.chart {
		width: calc(100% + 20px);
		transform: translate(-10px);
	}
}
</style>
