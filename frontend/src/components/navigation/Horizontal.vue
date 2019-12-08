<template>
	<div>
		<navigation-button link="overview"></navigation-button>
		<navigation-button link="budget"></navigation-button>
		<navigation-button link="transactions"></navigation-button>
	</div>
</template>

<script>
import NavigationButton from "@/components/navigation/NavigationButton";
import Navigation from "@/components/navigation/Navigation";

export default {
	name: "Horizontal",
	components: { NavigationButton }
};
</script>

<style scoped></style>
