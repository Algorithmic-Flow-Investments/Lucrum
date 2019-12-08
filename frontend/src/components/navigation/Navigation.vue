<template>
	<div class="column is-1" id="navigation">
		<div id="logo"><logo /></div>

		<navigation-button link="overview"></navigation-button>

		<navigation-button link="transactions"></navigation-button>

		<navigation-button link="budget"></navigation-button>

		<navigation-button link="accounts"></navigation-button>

		<navigation-button link="classification"></navigation-button>

		<data-button></data-button>
	</div>
</template>

<script>
import logo from "@/assets/logo.svg";
import NavigationButton from "@/components/navigation/NavigationButton";
import DataButton from "@/components/navigation/DataButton";

export default {
	name: "Navigation",
	components: {
		DataButton,
		NavigationButton,
		logo
	}
};
</script>

<style scoped>
	#navigation {
		position: relative;
	}
@media screen and (max-width: 768px) {
	.column {
		position: fixed;
		bottom: 0;
	}

	#logo {
		display: none;
	}
}

@media screen and (min-width: 768px) {
	#navigation {
		height: calc(100vh - 24px);
	}

	#logo {
		height: fit-content;
	}
}
</style>

<style>
.fillA {
	fill: #007d51 !important;
}

.fillB {
	fill: #005d57 !important;
}

.fillC {
	fill: #1eb980 !important;
}

.fillD {
	fill: #37efba !important;
}
</style>
