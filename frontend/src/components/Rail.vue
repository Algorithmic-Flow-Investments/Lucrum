<template>
<div class="sidebar mdc-theme--background">
	<mdc-icon style="width: 72px; padding-bottom: 20px">
		<logo/>
	</mdc-icon>


	<rail-button link="overview"/>

	<rail-button link="accounts"/>

	<rail-button link="budget"/>

	<rail-button link="transactions"/>

	<rail-button link="scheduled"/>

</div>
</template>

<script>
import RailButton from "@/components/RailButton";
import logo from "@/assets/logo.svg";

export default {
	name: "Rail",
	components: {
		RailButton,
		logo
	}
};
</script>

<style>
.sidebar {
	height: calc(100vh - var(--mdc-layout-grid-margin-desktop, 24px) * 2);
}

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
