<template>
	<mdc-layout-grid class="mdc-theme--background">
		<mdc-layout-cell desktop="5" tablet="8">
			<page-slot child="accounts">
				<accounts />
			</page-slot>
		</mdc-layout-cell>
		<mdc-layout-cell desktop="5" tablet="8">
			<page-slot child="scheduled">
				<scheduled />
			</page-slot>
		</mdc-layout-cell>
		<mdc-fab class="fab" icon="add"></mdc-fab>
	</mdc-layout-grid>
</template>

<script>
import Accounts from "@/components/Accounts";
import Scheduled from "@/components/Scheduled";
import PageSlot from "@/components/PageSlot";

export default {
	name: "Overview",
	components: {
		Accounts,
		Scheduled,
		PageSlot
	},
	methods: {
		handleScroll(a) {
			console.log(a);
		}
	},
	beforeMount() {
		window.addEventListener("scroll", this.handleScroll);
	},
	beforeDestroy() {
		window.removeEventListener("scroll", this.handleScroll);
	}
};
</script>

<style scoped>
.fab {
	bottom: 1rem;
	right: 1rem;
	position: fixed;
}
@media (min-width: 1024px) {
	.fab {
		bottom: 1.5rem;
		right: 1.5rem;
		position: fixed;
	}
}
</style>
