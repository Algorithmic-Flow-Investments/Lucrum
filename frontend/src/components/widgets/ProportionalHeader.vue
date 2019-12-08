<template>
	<div>
		<div class="main">{{ title }}</div>
		<div class="total">{{ total | numberWithCommas }}</div>
		<line-chart :data="chart"/>
	</div>
</template>

<script>
	import LineChart from "@/components/charts/LineChart";
	export default {
		name: "ProportionalHeader",
		props: ["title", "total", "chart"],
		components: {LineChart},
		filters: {
			numberWithCommas(x) {
				return x.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
			},
		}
	};
</script>

<style scoped lang="scss">
	@import "../../assets/colours";


	@each $colour in $greens {
	$i: index($greens, $colour);
		/deep/ .seg-#{$i} {
			background: $colour;
		}
	}

	.total {
		font-family: "Eczar", serif;
		color: white;
		font-size: 52px;
		line-height: 1;
	}

	.main {
		font-family: "Roboto Condensed", sans-serif;
		color: white;
		font-size: 16px;
	}

</style>
