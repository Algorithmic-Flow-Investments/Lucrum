<template>
	<div @click="go" class="nav-button">
		<b-icon :icon="icon" :class="{ unselected: !selected }" size="is-large" />
		<span class="name">{{ link }}</span>
	</div>
</template>

<script>
export default {
	name: "VerticalButton",
	props: ["link"],
	methods: {
		go() {
			if (this.link === "overview") {
				this.$router.push("/");
				return;
			}
			this.$router.push("/" + this.link);
		}
	},
	computed: {
		icon() {
			switch (this.link) {
				case "overview":
					return "home";
				case "accounts":
					return "university";
				case "budget":
					return "chart-pie";
				case "transactions":
					return "hand-holding-usd";
				case "scheduled":
					return "show_chart";
				case "classification":
					return "clipboard-list"
			}
			return "";
		},
		selected() {
			if (this.$route.path === "/" && this.link === "overview") {
				return true;
			}
			return this.$route.path.split("/")[1] === this.link;
		}
	}
};
</script>

<style scoped>
.mdc-icon {
	color: white;
	font-size: 42px;
	width: 100%;
	text-align: center;
}

div {
	padding-top: 42px;
	text-align: center;
}

.name {
	font-family: "Roboto Condensed", serif;
	color: white;
	display: block;
}

.unselected {
	color: #adadb1;
	cursor: pointer;
}

.flipY {
	transform: scaleY(-1);
}

.nav-button {
	display: inline-block;
	width: 100%;
}

@media screen and (max-width: 768px) {
	.nav-button {
		width: fit-content;
	}

	.name {
		display: inline-block;
	}
}
</style>
