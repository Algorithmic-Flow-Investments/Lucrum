<template>
	<div class="sidebar">
		<div class="logo">
			<logo />

			<navigation-button link="overview"></navigation-button>

			<navigation-button link="budget"></navigation-button>

			<navigation-button link="transactions"></navigation-button>
		</div>
	</div>
</template>

<script>
import logo from "@/assets/logo.svg";
import NavigationButton from "@/components/navigation/NavigationButton";

export default {
	name: "Vertical",
	components: {
		NavigationButton,
		logo
	}
};
</script>

<style scoped>
.sidebar {
	height: calc(100vh - 24px);
}
</style>

<style>
.logo_svg__fillA {
	fill: #007d51 !important;
}

.logo_svg__fillB {
	fill: #005d57 !important;
}

.logo_svg__fillC {
	fill: #1eb980 !important;
}

.logo_svg__fillD {
	fill: #37efba !important;
}
</style>
