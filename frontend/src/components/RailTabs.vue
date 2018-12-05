<template>
<div class="tabs">
	<rail-tab-button link="overview"/>

	<rail-tab-button link="accounts"/>

	<rail-tab-button link="budget"/>

	<rail-tab-button link="transactions"/>

	<rail-tab-button link="scheduled"/>
</div>
</template>

<script>
  import RailTabButton from "@/components/RailTabButton";

  export default {
	name: 'RailTabs',
	components: {
	  RailTabButton
	}
  }
</script>

<style scoped>
.tabs {
	height: 32px;
	padding: var(--mdc-layout-grid-margin-phone, 16px);
	display: flex;
	justify-content: space-between;
}
</style>
